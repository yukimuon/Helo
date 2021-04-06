from peewee import *
from mtencrypt import RSAgenerate, RSAimportPubkey, RSAencrypt, RSAdecrypt, getsha256
import string
import hashlib

db = SqliteDatabase('mt.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    uid = CharField(unique=True)
    upass = CharField()
    messages = CharField(default='')
    friends = CharField(default='')
    keypair = CharField(default='')

u = str(input("Delete uid? \n"))
for user in User.select().where(User.uid == u):
    print("UID:",user.uid, "\nPASS:", user.upass,"\nMessage:\n", user.messages, "\n------------------\nKeypair:", user.keypair)
    confirm = str(input("Confirm? y/n\n"))
    if confirm == "y":
        user.delete_instance()
        user.save()