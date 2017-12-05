#!/usr/bin/env python
# -*- coding: utf-8 -*-
# AES/CBC/pkcs5padding， 128位 ，密钥KLambdaDaiFaNong ，偏移量0102030405060708 
from Cryptodome.Cipher import AES
import base64

'''
封装lambda的加密和解密方法
'''

key_dict =      {
                'omega_test':'KOmegaDaiFaNongO',
                'lambda_test':'KLambdaDaiFaNong',
                'omega':'k2%&qOnL4x9mayP#',
                'lambda':'k2%&qOnL4x9mayP#'
                }

class LambdaEncrpt():
    def __init__(self,key,iv='0102030405060708'):
        self.key = key.encode()
        self.iv  = iv.encode()
        self.mode = AES.MODE_CBC
        
    def _encrypt(self,source):       
        BS = 16
        pad_it = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        generator = AES.new(self.key, self.mode, self.iv)
        crypt = generator.encrypt(pad_it(source).encode())
        cryptedStr = base64.b64encode(crypt)
        print(cryptedStr.decode())
        return cryptedStr.decode()
    def _decrypt(self,text):
        unpad = lambda s : s[0:-ord(s.decode()[-1])]
        generator = AES.new(self.key, self.mode, self.iv)
        recovery = generator.decrypt(base64.b64decode(text))
        decryStr = unpad(recovery)
        print(decryStr.decode())
        return decryStr.decode()


if __name__ == '__main__':
    key = key_dict.get('lambda_test')
    pc = LambdaEncrpt(key)
    pc._encrypt('410825199204257544')
    pc._decrypt('/jBhRV13uDG7QoFwDrqCHyl/SCVzvVOJxCUQyffgnME=')