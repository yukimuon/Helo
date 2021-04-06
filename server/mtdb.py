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

def adduser(uid, upass):
    try:
        if User.select().where(User.uid==uid):
            return "FAILED"
        else:
            if len(uid) <6:
                uid.translate(str.maketrans('', '', string.punctuation))
                oneperson = User(uid=uid, upass=upass, messages="INITMSG;\n")
                oneperson.save()
                return "SUCCESSFUL"
    except:
        return "FAILED"

def pushmsg(sender, receiver, msg):
    print(sender,"->",receiver,":",msg)
    try:
        for user in User.select().where(User.uid == receiver):
            msg_record = sender+":"+msg+";\n"
            user.messages += msg_record
            user.save()  
            return "SEND-SUCC"
    except:
        return "SEND-FAIL"

def popmsg(uid,upass):
    try:
        for user in User.select().where(User.uid == uid):
            if upass == user.upass:
                msg = user.messages
                user.messages = ""
                user.save()
                return "CLEARED"
        return "CLEAR-NOTFOUND"
    except:
        return "CLEAR-ERR"

def auth(uid,upass):
    try:
        for user in User.select().where(User.uid == uid):
            print("AUTH->",upass == user.upass)
            return upass == user.upass
        return False
    except:
        return False
        

def getfriends(uid,upass):
    try:
        for user in User.select().where(User.uid == uid):
            if upass == user.upass:
                return user.friends.split(",")
        return
    except:
        return 


def addfriends(uid, upass, friendid):
    try:
        for user in User.select().where(User.uid == uid):
            if upass == user.upass:
                user.friends += ","
                user.friends += friendid          
                user.save()       
                return True
    except:
        return False



def updatekey(uid, upass, token):
    try:
        for user in User.select().where(User.uid == uid):
            if upass == user.upass:
                user.keypair = token
                user.save()       

            return True
    except:
        return False

def encmsg(uid,upass):
    try:
        for user in User.select().where(User.uid == uid):
            if upass == user.upass:
                token = user.keypair
                mes = user.messages
                n=token.strip().split(",")[0]
                e=token.strip().split(",")[1]
                # print("------------")
                # print(n,e)        
                # print(mes)  
                cli_pubk=RSAimportPubkey(n,e)
                enc = RSAencrypt(RSAimportPubkey(n,e), mes)
                print("Enc to len",len(enc))
                return enc
    except:
        print("DB-ENCERR", sys.exc_info()[0])

def RSAparser(buf):
   # Just a parser
#    print(buf)
   msg=buf.decode("utf-8")
   certsha = msg.split("-")[-1]
   uname = msg.split(":")[0]
   pubkey=msg.split(":")[1].split("-")[0]
   return rsasigcheck(pubkey, uname, certsha)

def rsasigcheck(msg, uid, certsha):
    for user in User.select().where(User.uid == str(uid)):
        upas = user.upass
        s=str(msg)+str(uid)+str(upas)
        shacla = getsha256(s)
        # print(uid, certsha, shacla)
        if (certsha in shacla) or (shacla in certsha):
            user.keypair = msg
            user.save()
        return b"KEYVERI-SUCC"

    return b"KEYVERI-FAIL"


def handler(msg_b):
    try:
        msg = msg_b.decode("utf-8")
        msg.replace("'","")
        msg.replace(",","")
        msg_args = msg.strip().split("-")
        if len(msg_args) != 3:
            return b"SYNTAXERR"
        cmd = msg_args[0]
        uid = msg_args[1]
        upass = msg_args[2]
        print("CLI:",uid, upass, cmd)
        if cmd == "REGISTER":
            return bytes("REGISTER-"+str(adduser(uid, upass)),"utf-8")
        if not(auth(uid, upass)):
            print("AUTHERR")
            return b"AUTHERR"
        # print(cmd, uid, upass)
        if cmd == "FETCH":
            return encmsg(uid, upass)
        if cmd.split(":")[0] == "ADD":
            friendid = cmd.split(":")[1]
            return bytes("ADDFRIEND-"+ str(addfriends(uid, upass, friendid)),"utf-8")
        if cmd == "CLEAR":
            return bytes(popmsg(uid,upass),"utf-8")
        if cmd.split(":")[0] == "SEND":
            tar = cmd.split(":")[1]
            msgts = cmd.split(":")[2]
            if auth(uid, upass):
                return bytes(pushmsg(uid, tar, msgts), "utf-8")
        # print(msg)
        return "SYNTAXERR"
    except:
        return "UNKNOWN-ERR"

    
