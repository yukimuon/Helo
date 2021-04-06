from gui_main import *
import cv2
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
from Crypto.PublicKey.RSA import construct
from network import *
from mtencrypt import RSAgenerate, RSAencrypt, RSAdecrypt, RSAimportPubkey
from Crypto.Cipher import AES
import time
class Store:
    def __init__(self):
        captureDevice = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.uid = ""
        self.password = ""

        # Crypto keys
        self.RSAkeypair = RSAgenerate(2048)
        self.session_RSApubkey = self.RSAkeypair.publickey()
        self.session_AESkey = ""

        # Addrs
        self.server_addr = ""

Store = Store()


response = HANDSHAKE("192.168.239.128", 65000)
server_n=response.split(",")[0]
server_e=response.split(",")[1]

kp = RSAgenerate(4096)
n = str(kp.publickey().n)
e = str(kp.publickey().e)

print("LINE6")
response = SENDRSA("192.168.239.128", 65003, n, e, "user", "pass")
print("RESPONSE:",response)
print("----------")
response = SEND("192.168.239.128", 65001, server_n, server_e, "FETCH-user-pass")
print("RESPONSE:",response)

print(len(response))
print(n,e)
