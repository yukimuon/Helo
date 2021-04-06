from translate import Translator
from mtencrypt import RSAgenerate, RSAencrypt, RSAdecrypt, RSAimportPubkey


def tr(tr_lang, msg):
    translator= Translator(to_lang=tr_lang)
    if type(msg) == str:
        result = translator.translate(msg)
        return result
    else:
        return msg

def tr_dec(tr_lang, msg, kp):
    translator= Translator(to_lang=tr_lang)
    if type(msg) == str:
        result = translator.translate(msg)
        return result
    else:
        try:
            dec = RSAdecrypt(kp, msg)
            return dec
        except:
            return result

