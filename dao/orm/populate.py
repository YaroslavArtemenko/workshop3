from dao.orm.model import *
from dao.db import OracleDb

db = OracleDb()

Base.metadata.create_all(db.sqlalchemy_engine)


session = db.sqlalchemy_session

# clear all tables in right order
session.query(ormUserHobby).delete()
session.query(ormHobby).delete()
session.query(ormUser).delete()


# populate database with new rows

a = ormUser( user_name="a",
               user_email='a@gmail.com',
               user_phone='+38099999999'
               )



b = ormUser( user_name="b",
               user_email='b@gmail.com',
                user_phone='+38903948'
               )


c = ormUser( user_name="c",
               user_email='c@gmail.com',
                user_phone='+34343543'
               )


d = ormUser( user_name="d",
               user_email='d@gmail.com',
                user_phone='+34324325432'
               )


Football = ormHobby(hobby_name='Football')
bar = ormHobby(hobby_name='bar')
club = ormHobby(hobby_name='club')
fly = ormHobby(hobby_name='fly')

# create relations
a.orm_hobbys.append(bar)
a.orm_hobbys.append(Football)
a.orm_hobbys.append(club)
a.orm_hobbys.append(fly)

b.orm_hobbys.append(bar)

c.orm_hobbys.append(club)

# insert into database
session.add_all([Football,club,bar, fly,a,b,c,d])

session.commit()