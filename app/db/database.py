from sqlalchemy import *
import uuid
from datetime import datetime,timedelta
import json

from services.rand_name import randName

def id_create() -> str:
    result = uuid.uuid1()
    # print(result)
    return result

def current_time():
    currentTime = datetime.now()
    return currentTime

def daysPlus30():
    result = current_time() + timedelta(days=30)
    return result




db = create_engine('sqlite:///tutorial.db')

db.echo = False  # Try changing this to True and see what happens

metadata = BoundMetaData(db)

todos =Table('todos', metadata
            ,Column('id', String(50, primary_key=True, default=id_create()))
            ,Column('title', String(150))
            ,Column('description', String(500))
            ,Column('isComplete', Boolean(defualt=False))
            ,Column('dateDue', String(50, default=daysPlus30())
            ,Column('dateCreate', String(50, default=current_time())
            ,Column('dateComplete', String(50, default=None))
            ,Column('userId', String(50, default=randName()))
            )



users = Table('users', metadata,
    Column('user_id', Integer, primary_key=True),
    Column('name', String(40)),
    Column('age', Integer),
    Column('password', String),
)
users.create()


i = users.insert()
i.execute(name='Mary', age=30, password='secret')
i.execute({'name': 'John', 'age': 42},
          {'name': 'Susan', 'age': 57},
          {'name': 'Carl', 'age': 33})

s = users.select()
rs = s.execute()

row = rs.fetchone()
print 'Id:', row[0]
print 'Name:', row['name']
print 'Age:', row.age
print 'Password:', row[users.c.password]

for row in rs:
    print row.name, 'is', row.age, 'years old'