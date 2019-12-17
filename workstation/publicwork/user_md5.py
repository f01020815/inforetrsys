import hashlib

def pwd_encrypt(password):
    md5=hashlib.md5()
    #password.encode()，对password进行二进制编码，返回一个二进制值
    md5.update(password.encode())
    result=md5.hexdigest()#返回十六进制数据字符串值
    return result