# -*- coding: utf-8 -*-

import base64

from Crypto.Cipher import AES

BLOCK_SIZE = 16


def pkcs5_pad(s):
    n = BLOCK_SIZE - len(s) % BLOCK_SIZE
    return s + n * chr(n)


def pkcs5_unpad(s):
    return s[0:-ord(s[-1])]


class AESCipher(object):
    def __init__(self, key):
        self.key = key

    def encrypt(self, data):
        cipher = AES.new(self.key)
        encrypted = cipher.encrypt(pkcs5_pad(data))
        return base64.b64encode(encrypted).decode()

    def decrypt(self, data):
        cipher = AES.new(self.key)
        decrypted = cipher.decrypt(base64.b64decode(data)).decode()
        return pkcs5_unpad(decrypted)


aes = AESCipher(b'\x96\xf7h\xe3\xd4\xedH\x1c3\xe7\xd6b\x85\x96\xf3\xf2')
