from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class ormUser(Base):
    __tablename__ = 'orm_user'
    user_name = Column(String(20), nullable=False)
    user_email = Column(String(40), primary_key=True)
    user_phone = Column(String(15), nullable=False)


    orm_hobbys = relationship('ormHobby', secondary='orm_user_hobby')


class ormHobby(Base):
    __tablename__ = 'orm_hobby'
    hobby_name = Column(String(40), primary_key=True)

    orm_users = relationship('ormUser', secondary='orm_user_hobby')


class ormUserHobby(Base):
    __tablename__ = 'orm_user_hobby'

    user_email = Column(String(40),ForeignKey('orm_user.user_email'),primary_key = True)
    hobby_name = Column(String(40), ForeignKey('orm_hobby.hobby_name'), primary_key=True)




