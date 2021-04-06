from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
from Crypto.PublicKey.RSA import construct
from Crypto.Cipher import AES
import hashlib

def RSAgenerate(length):
   keyPair = RSA.generate(length)

   pubKey = keyPair.publickey()
   pubKeyPEM = pubKey.exportKey()
   privKeyPEM = keyPair.exportKey()
   return keyPair

def RSAimportPubkey(n,e):
   return construct((int(n), int(e)))

def RSAencrypt(pubkey, msg):
   encryptor = PKCS1_OAEP.new(pubkey)
   if type(msg)==bytes:
      encrypted = encryptor.encrypt(msg)
   else:
      encrypted = encryptor.encrypt(bytes(msg, "utf-8"))
   return encrypted

def RSAdecrypt(keyPair, msg):
   try:
      decryptor = PKCS1_OAEP.new(keyPair)
      decrypted = decryptor.decrypt(msg)
      return decrypted
   except:
      return "Decryption failed"

def getsha256(s):
   m = hashlib.sha256()
   m.update(bytes(s,'utf-8'))
   return m.hexdigest()