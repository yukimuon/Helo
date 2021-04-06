import socket
from mtencrypt import *

def HANDSHAKE(HOST, PORT):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, int(PORT)))
            data = s.recv(1024)
        return data.decode("utf-8")
    except:
        return "HANDSHAKE-ERR"

def SEND(HOST, PORT, N, E, msg):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, int(PORT)))
            keyp = RSAimportPubkey(N, E)
            msg_e = RSAencrypt(keyp, msg)
            s.sendall(msg_e)
            print(len(msg_e),"bytes sent")
            buf = s.recv(1024)
            return buf
    except Exception as e:
        return "SEND-ERR:"+str(e)

def SENDRSA(HOST, PORT, N, E, uid, upass):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            msg=str(N)+","+str(E)+uid+upass
            certsha = getsha256(msg)
            msg = uid+":"+str(N)+","+str(E)+"-"+certsha
            s.connect((HOST, int(PORT)))
            s.sendall(bytes(msg,"utf-8"))
            print(len(msg),"bytes RSA Key sent")
            data = s.recv(512)
            s.close()
            return data
    except Exception as e:
        return "SENDRSA-ERR:"+str(e)