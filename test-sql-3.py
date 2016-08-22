import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql://root:pass@127.0.0.1/test?charset=utf8', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    fullname = Column(String(40))
    password = Column(String(40))

    def __repr__(self):
       return "<User(name='%s', fullname='%s', password='%s')>" % (
                            self.name, self.fullname, self.password)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

print 'start query'
session = Session()
q = session.query(User).all()
print 'start print'
for t in q:
    print t.name
