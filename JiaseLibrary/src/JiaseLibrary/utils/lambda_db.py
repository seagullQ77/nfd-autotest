# -*- coding: utf-8 -*-
import pymysql
from .lambda_encrpt import LambdaEncrpt

'''
封装操作lambda 数据库的相关方法 
'''

class LambdaDbCon():

    def __init__(self, lambda_db_host, lambda_db_user, lambda_db_passwd, lambda_db_port, lambda_db_charset,
                 env='lambda_test'):
        self.db_host = lambda_db_host
        self.db_user = lambda_db_user
        self.db_passwd = lambda_db_passwd
        self.db_port = lambda_db_port
        self.db_charset = lambda_db_charset
        self.env = env
        self.lambda_encrpt = LambdaEncrpt(env)

    def __conn(func):
        def wrapper(self, *args, **kwargs):
            self.__connect = pymysql.connect(host=self.db_host, user=self.db_user, passwd=self.db_passwd,
                                             port=self.db_port, charset=self.db_charset)
            self.__cursor = self.__connect.cursor()
            __wrapper = func(self, *args, **kwargs)
            self.__close()
            return __wrapper

        return wrapper

    def __close(self):
        self.__cursor.close()
        self.__connect.close()

    @__conn
    def check_db(self, sql, value=1):
        '''
        查询数据库中是否存在对应的记录
        sql以 SELECT COUNT(*) 进行查询满足条件的记录数
        :param sql:
        :return:0:成功/1:失败
        '''
        self.__connect.select_db('lambda')
        self.__cursor.execute(sql)
        db_value = self.__cursor.fetchone()[0]
        if db_value == value:
            return True
        else:
            return False

    @__conn
    def exec_sql(self, sql):
        '''
        执行sql
        :param sql:
        '''
        self.__connect.select_db('lambda')
        self.__cursor.execute(sql)
        self.__connect.commit()

    @__conn
    def update_sys_user_password(self, account):
        self.__connect.select_db('lambda')
        en_account = self.lambda_encrpt._encrypt(account)
        # query_sql = "SELECT * FROM `sys_user` WHERE account='%s'" %en_account
        update_sql = "UPDATE sys_user SET user_password='$2a$11$P3GPFasiq.D/2QJhODL73uvfSyxKfu6SMftQp8w946YpDMOiIgPCy' WHERE account ='%s'" % en_account
        self.__cursor.execute(update_sql)
        self.__connect.commit()


if __name__ == '__main__':
    testdb = LambdaDbCon('10.1.60.107')
    # testdb.update_sys_user_password('15228585245')
    testdb.check_sql("select count(*) from sys_user WHERE  real_name ='admin1'")
