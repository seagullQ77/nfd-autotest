# -*- coding: utf-8 -*-
import pymysql
from lambda_encrpt import LambdaEncrpt
'''
封装操作lambda 数据库的相关方法 
'''
class LambdaDbCon():

    def __init__(self,lambda_db_host,lambda_db_user,lambda_db_passwd,lambda_db_port,lambda_db_charset,env='lambda_test'):
        self.db_host = lambda_db_host
        self.db_user = lambda_db_user
        self.db_passwd = lambda_db_passwd
        self.db_port = lambda_db_port
        self.db_charset = lambda_db_charset
        self.env = env
        self.connect = pymysql.connect(host=self.db_host, user=self.db_user, passwd=self.db_passwd, 
                                    port=self.db_port,charset=self.db_charset)
        self.cursor = self.connect.cursor()
        self.lambda_encrpt = LambdaEncrpt(env)

    def check_db(self,sql):
        '''
        查询数据库中是否存在对应的记录
        sql以 SELECT COUNT(*) 进行查询满足条件的记录数
        :param sql:
        :return:0:成功/1:失败
        '''
        self.connect.select_db('lambda')
        self.cursor.execute(sql)
        value = self.cursor.fetchone()[0]
        self.cursor.close()
        self.connect.close()
        if value == 1:
            return 0
        else:
            return 1

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
    testdb =  LambdaDbCon('10.1.60.107')
    # testdb.update_sys_user_password('15228585245')
    testdb.check_sql("select count(*) from sys_user WHERE  real_name ='admin1'")
    