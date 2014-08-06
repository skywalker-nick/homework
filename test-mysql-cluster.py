import sqlalchemy as sa
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, Session
import random
import re
import time


ENGINES = {
    'master1': 'mysql+mysqlconnector://root:password@192.168.3.188/testtest',
    'master2': 'mysql+mysqlconnector://root:password@192.168.3.189/testtest',
    'slave1': 'mysql+mysqlconnector://root:password@192.168.3.191/testtest',
    'slave2': 'mysql+mysqlconnector://root:password@192.168.3.191/testtest',
}


master_keys = []
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

    if re.match(r"^master", key):
        master_keys.append(key)


class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None):
        if self._name:
            return engines[self._name]
        elif self._flushing:
            return engines[
                random.choice(master_keys)
            ]
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


Session = sessionmaker(autocommit=True,
                       autoflush=False,
                       expire_on_commit=False,
                       class_=RoutingSession)
db_session = Session()
Base = declarative_base()


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

    def __repr__(self):
        return "<Entry('%s','%s','%s')>" \
               % (self.id, self.title, self.text)


for (k, v) in engines.items():
    init_db(v)


print '############################### master insertion ################################'
with db_session.begin(subtransactions=True):
    db_session.add_all([
        Entries(title='entry_a', text='hoge'),
        Entries(title='entry_b', text='fuga'),
        Entries(title='entry_c', text='piyo'),
    ])

print '###################### select (slave) ######################'
rs = db_session.query(Entries).all()
print_rs(rs)
rs = db_session.query(Entries).all()
print_rs(rs)
rs = db_session.query(Entries).all()
print_rs(rs)

print '######################## master insersion ############################'
with db_session.begin(subtransactions=True):
    db_session.add_all([Entries(title=random.randint(1, 100), text=random.randint(1, 100)) for i in xrange(10)])
    rs = db_session.query(Entries).all()
    print_rs(rs)

print '######################## transaction insertion #############################'
with db_session.begin(subtransactions=True):
    entry = Entries(title='entry_d', text='nick')
    db_session.add(entry)

print '######################## transaction mixed operations 1 #############################'
with db_session.begin(subtransactions=True):
    query = db_session.query(Entries).filter_by(title='entry_b').first()
    print query
    query.text = 'changed'
    query = db_session.query(Entries).filter_by(title='entry_b').first()
    print query

print '######################## transaction mixed operations 2 #############################'
with db_session.begin(subtransactions=True):
    query = db_session.query(Entries).delete()
    rs = db_session.query(Entries).count()
    print 'count: %d' % rs

print '######################## verify transaction #############################'
with db_session.begin(subtransactions=True):
    rs = db_session.query(Entries).count()
    print 'count 1: %d' % rs

with db_session.begin(subtransactions=True):
    rs = db_session.query(Entries).count()
    print 'count 2: %d' % rs

with db_session.begin(subtransactions=True):
    rs = db_session.query(Entries).count()
    print 'count 3: %d' % rs
