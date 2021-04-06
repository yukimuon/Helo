from mtdb import *

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    uid = CharField(unique=True)
    upass = CharField()
    messages = CharField(default='')
    friends = CharField(default='')
    keypair = CharField(default='')

db = SqliteDatabase('mt.db')
db.connect()
db.create_tables([User])