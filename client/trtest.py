from tr import *
from mtencrypt import RSAgenerate, RSAencrypt, RSAdecrypt, RSAimportPubkey

print(tr("en", "你好"))
print(tr("ZH-CN", "What is the time fo meeting"))

kp = RSAgenerate(2048)
n = kp.publickey().n
e = kp.publickey().e
print(n)
pub=RSAimportPubkey(n,e)

mes = "Hello?."
enc = RSAencrypt(pub, mes)
print(enc)
dec = tr_dec("ZH-CN",enc,kp)
print(dec)