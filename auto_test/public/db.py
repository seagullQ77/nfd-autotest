#!/usr/bin/env python3
#coding=utf-8

import os
import sys
import pymysql

current_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_path)
import conf

class mysql:

    def __init__(self):
        self.host = conf.get_conf('db','host')
        self.user = conf.get_conf('db','user')
        self.passwd = conf.get_conf('db','passwd')
        self.port = int(conf.get_conf('db','port'))
        self.charset = conf.get_conf('db','charset')

    def connect(self):
        try:
            conn = pymysql.connect(host=self.host,user=self.user,passwd=self.passwd,port=self.port,charset=self.charset)
        except Exception as e:
             print(e)
        return conn

    def query(self,sql):
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(sql)
            value = cur.fetchone()
            self.close(conn,cur)
        except Exception as e:
            print(e)
        return value[0]

    def query_dict(self,sql):
        try:
            conn = self.connect()
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute(sql)
            value = cur.fetchone()
            self.close(conn,cur)
        except Exception as e:
            print(e)
        return value

    def close(self,conn,cur):
        cur.close()
        conn.close()


if __name__ == '__main__':
    app = mysql()
