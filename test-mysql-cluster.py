import sqlalchemy as sa
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, Session
import random
import re
import time


ENGINES = {
    'master': 'mysql+mysqlconnector://root:password@192.168.3.188/testtest',
    'slave1': 'mysql+mysqlconnector://root:password@192.168.3.189/testtest',
    'slave2': 'mysql+mysqlconnector://root:password@192.168.3.191/testtest',
}


slave_keys = []
engines = {}
for key in ENGINES.keys():
    engines[key] = create_engine(
            "%s" % ENGINES[key],
            encoding='utf-8',
            logging_name=key,
            echo=True)
    if re.match(r"^slave", key):
        slave_keys.append(key)


class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None ):
        if self._name:
            return engines[self._name]
        elif self._flushing:
            return engines['master']
        else:
            return engines[
               random.choice(slave_keys)
            ]
    _name = None
    def using_bind(self, name):
        s = RoutingSession()
        vars(s).update(vars(self))
        s._name = name
        return s


db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         class_=RoutingSession))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db(s):
    Base.metadata.create_all(s)


def print_rs(rs):
    print rs


class Entries(Base):
    __tablename__ = 'entries'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }   
    
    id = Column('id', Integer, primary_key=True)
    title = Column(Text)
    text = Column(Text)


for (k, v) in engines.items():
    init_db(v)


print '############################### insert ################################'
db_session.add_all([
    Entries(title='entry_a', text='hoge'),
    Entries(title='entry_b', text='fuga'),
    Entries(title='entry_c', text='piyo'),
])
db_session.commit()

print '###################### select (slave1 or slave2) ######################'
rs = db_session.query(Entries).all()
print_rs(rs)
rs = db_session.query(Entries).all()
print_rs(rs)
rs = db_session.query(Entries).all()
print_rs(rs)

print '######################## fix master select ############################'
rs = db_session().using_bind("master").query(Entries).first()
print_rs(rs)

db_session.add_all([Entries(title=random.randint(1, 100), text=random.randint(1, 100)) for i in xrange(10)])
db_session.commit()

print '######################## transaction test #############################'
with db_session.begin(subtransactions=True):
    entry = Entries(title='entry_d', text='nick')
    db_session.add(entry)

with db_session.begin(subtransactions=True):
    query = db_session.query(Entries).filter_by(title='entry_b').one()
    query.text = 'changed'
