import socket
from mtencrypt import *
import threading
import time
from mtdb import *

kp = RSAgenerate(2048)

n = kp.publickey().n
e = kp.publickey().e


def COMMINICATION(HOST, PORT, N, E, bts):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
        serversocket.bind(("", int(PORT)))
        serversocket.listen()
        while True:
            conn, addr = serversocket.accept()
            buf = conn.recv(1024)
            msg = RSAdecrypt(kp, buf)
            btsrespo = handler(msg)
            if type(btsrespo)!= bytes:
                btsrespo=bytes(btsrespo,"utf-8")
            print(len(btsrespo),"bytes sent")
            conn.sendall(btsrespo)
            conn.close()


def UPDATERSA(HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
        serversocket.bind(("", int(PORT)))
        serversocket.listen()
        while True:
            conn, addr = serversocket.accept()
            buf = conn.recv(2048)
            print("RSA Key received")
            conn.sendall(RSAparser(buf))
            conn.close()


def HANDSHAKE(HOST, PORT, N, E):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
        serversocket.bind(("", int(PORT)))
        serversocket.listen()
        while True:
            conn, addr = serversocket.accept()
            with conn:
                print('Connected by', addr)
                keyp = str(N) + "," + str(E)
                conn.sendall(bytes(keyp, "utf-8"))
                conn.close()        

job1 = threading.Thread(target=HANDSHAKE, args=('192.168.239.128', 65000 , n, e))
job2 = threading.Thread(target=COMMINICATION, args=('192.168.239.128', 65001 , n, e, 4096))
job3 = threading.Thread(target=UPDATERSA, args=('192.168.239.128', 65003))
job1.start()
job2.start()
job3.start()
