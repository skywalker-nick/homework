import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random
import time

DB_PATH = 'mysql://root:6cead92a385e4997@192.168.247.188/remote_mgmt'

Base = declarative_base()

class Host(Base):
    __tablename__ = 'hosts'

    id = sa.Column(sa.String(36),
                   primary_key=True)
    ip = sa.Column(sa.String(255))
    hostname = sa.Column(sa.String(255))
    port = sa.Column(sa.Integer)
    description = sa.Column(sa.String(255))
    username = sa.Column(sa.String(255))
    password = sa.Column(sa.String(255))

    def __init__(self, data):
        self.id = data['id']
        self.ip = data['ip']
        self.hostname = data['hostname']
        self.port = data['port']
        self.description = data['description']
        self.username = data['username']
        self.password = data['password']

    def __init__(self, id, ip, hostname, port, desp, username, password):
        self.id = id
        self.ip = ip
        self.hostname = hostname
        self.port = port
        self.description = desp
        self.username = username
        self.password = password

    def __repr__(self):
        return "<Host('%s','%s','%s','%s','%s', '%s', '%s')>" \
               % (self.id, self.ip, self.hostname,
                  self.port, self.description,
                  self.username, self.password)

class IpmiDBHelper(object):
    def __init__(self):
        self.engine = sa.create_engine(DB_PATH, echo=True)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine,
                                    autocommit=True,
                                    expire_on_commit=False)

    @property
    def db_engine(self):
        return self.engine

    def db_session(self):
        return self.session()


if __name__ == '__main__':
    db_engine = IpmiDBHelper()
    session = db_engine.db_session()

    with session.begin(subtransactions=True):
        query = session.query(Host).filter_by(id='1111222233334444').one()

    print 'query: ' + str(query) + '\n\n'
