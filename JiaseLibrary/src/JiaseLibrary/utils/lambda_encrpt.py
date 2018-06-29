#!/usr/bin/env python
# -*- coding: utf-8 -*-
# AES/CBC/pkcs5padding， 128位 ，密钥KLambdaDaiFaNong ，偏移量0102030405060708 
from Crypto.Cipher import AES
import base64

'''
封装lambda的加密和解密方法
'''

class LambdaEncrpt():
    key_dict = {
        'omega_test': 'KOmegaDaiFaNongO',
        'lambda_test': 'KLambdaDaiFaNong',
        'omega': 'k2%&qOnL4x9mayP#',
        'lambda': 'k2%&qOnL4x9mayP#'
    }

    def __init__(self,env):
        key = self.key_dict.get(env)
        iv = '0102030405060708'
        self.key = key.encode()
        self.iv  = iv.encode()
        self.mode = AES.MODE_CBC
        
    def _encrypt(self,source):       
        slen = len(source.encode('utf-8'))%16
        pad_it = lambda s: s + (16-slen) *chr(16-slen)
        generator = AES.new(self.key, self.mode, self.iv)
        crypt = generator.encrypt(pad_it(source).encode())
        cryptedStr = base64.b64encode(crypt)
        return cryptedStr.decode()
    def _decrypt(self,text):
        generator = AES.new(self.key, self.mode, self.iv)
        recovery = generator.decrypt(base64.b64decode(text))
        unpad = lambda s : s[0:-ord(s[-1])]
        decryStr =unpad ((recovery.decode()))
        return decryStr


if __name__ == '__main__':
    pc = LambdaEncrpt('lambda_test')
    print(pc._encrypt('GreenPolls测试'))
    print(pc._decrypt('VjlVB1WhVQZOMxXIF+I+TGK4VzqamhonfjsALU4MKNw='))
    #VjlVB1WhVQZOMxXIF+I+TGK4VzqamhonfjsALU4MKNw=
