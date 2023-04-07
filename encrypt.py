import random
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def random_string(length):
    """生成指定长度的随机字符串"""
    aes_chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
    return ''.join(random.choice(aes_chars) for _ in range(length))

def get_aes_string(data, key0, iv0):
    key = key0.strip().encode('utf-8')
    iv = iv0.strip().encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pad = AES.block_size - len(data) % AES.block_size
    data = data + pad * chr(pad)
    encrypted = cipher.encrypt(data.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

def encrypt_AES(data, aes_key):
    if not aes_key:
        return data
    encrypted = get_aes_string(random_string(64)+data, aes_key, random_string(16))
    return encrypted

def encrypt_password(pwd0, key):
    return encrypt_AES(pwd0, key)

if __name__ == '__main__':
    pass
