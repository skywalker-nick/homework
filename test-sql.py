import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql://root:password@127.0.0.1/test?charset=utf8', echo=True)
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

for i in range(20):
    user = User(name='abc-%s' % str(i), fullname='ABC-%s' % str(i), password='edspassword')
    session.add(user)
session.commit()

print 'start query'
session = Session()
q = session.query(User)
print 'start filter'
t = q.filter_by(name='abc-11')
print 'start print'
for i in t:
    print t
