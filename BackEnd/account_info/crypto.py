from Crypto.Cipher import AES
import base64
import sys
sys.path.append("..")
from BackEnd import settings

def _pad(s): return s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size) 
def _cipher():
    key = settings.SECRET_KEY
    # return AES.new(key=key, mode=AES.MODE_CBC, IV=iv)
    return AES.new(key=key[:32], mode=AES.MODE_CBC, IV=key[:16])
 
def encrypt(data):
    if settings.ENABLE_CRYPTO:
        return _cipher().encrypt(_pad(data))
    return data
    
def decrypt(data):
    if settings.ENABLE_CRYPTO:
        return _cipher().decrypt(data)
    return data


if __name__ == '__main__':
    # print(encrypt('zhangshanfeng'))
    print('Python encrypt: ' + str(base64.b64encode(encrypt('zhangshanfeng'))))
    print('Python decrypt: ' + str(decrypt(base64.b64decode('FSfhJ/gk3iEJOPVLyFVc2Q=='))))