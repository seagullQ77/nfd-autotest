# -*- coding: utf-8 -*-
import pymysql
from lambda_encrpt import LambdaEncrpt
'''
封装操作lambda 数据库的相关方法 
'''
class LambdaDbCon():
    
    def __init__(self,host):
        self.db_host=host
        self.db_user='SecureTeam'
        self.db_passwd='Aqdy(%@#'
        self.db_port=9527
        self.db_charset="utf8"
        self.connect = pymysql.connect(host=self.db_host, user=self.db_user, passwd=self.db_passwd, 
                                    port=self.db_port,charset=self.db_charset)
        self.cursor = self.connect.cursor()
        self.lambda_encrpt = LambdaEncrpt()
          
    def update_sys_user_password(self,account):       
        self.connect.select_db('lambda')
        en_account = self.lambda_encrpt._encrypt(account)
        # query_sql = "SELECT * FROM `sys_user` WHERE account='%s'" %en_account
        update_sql = "UPDATE sys_user SET user_password='$2a$11$P3GPFasiq.D/2QJhODL73uvfSyxKfu6SMftQp8w946YpDMOiIgPCy' WHERE account ='%s'" %en_account
        self.cursor.execute(update_sql)
        self.connect.commit()    
        self.cursor.close()
        self.connect.close()

if __name__ == '__main__':
    testdb =  LambdaDbCon('10.1.60.57')
    testdb.update_sys_user_password('15228585245')
    