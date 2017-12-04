#!/usr/bin/env python
# -*- coding: utf-8 -*-
# AES/CBC/pkcs5padding， 128位 ，密钥KLambdaDaiFaNong ，偏移量0102030405060708 
from Crypto.Cipher import AES
import base64

'''
封装lambda的加密和解密方法
'''
class LambdaEncrpt():
    def __init__(self):
        self.key = 'KLambdaDaiFaNong'
        self.iv  = '0102030405060708'
        self.mode = AES.MODE_CBC
        
    def _encrypt(self,source):       
        BS = 16
        pad_it = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
        generator = AES.new(self.key, self.mode, self.iv)
        crypt = generator.encrypt(pad_it(source))   
        cryptedStr = base64.b64encode(crypt) 
        return cryptedStr
    
    def _decrypt(self,text):
        unpad = lambda s : s[0:-ord(s[-1])]
        generator = AES.new(self.key, self.mode, self.iv)
        recovery = generator.decrypt(base64.b64decode(text))
        decryStr = unpad(recovery)
        print decryStr
        return decryStr   
 
if __name__ == '__main__':
    # Lambda秘钥:KLambdaDaiFaNong   Omega秘钥 KOmegaDaiFaNongO
    pc = prpcrypt()
    
    #pc.encrypt('杭州市萧山区人民法院测试法院1123120012321测试')
    #pc.encrypt('（2017）浙0109执2173号测试11232132')
    #pc.encrypt('执行标的:123213212132134')
    #pc.encrypt('测试执行状态')
    pc.encrypt('18681579904')
    pc.encrypt('6212267867939820788')
    pc.decrypt('zkQdZsp/m3jqMM5Oos3v/OQyrFwyvRcGTP0TKyPJqMk=')
    