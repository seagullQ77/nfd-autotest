#!/usr/bin/env python3
#coding=utf-8

import os
import sys
import json
import unittest
current_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_path)
import db

def check_code(ret,expect_code):
    try:
        ret_dic = json.loads(ret)
    except Exception as e:
        print(e)
    actual_code = ret_dic.get('statusCode')
    if str(expect_code) == '0':
        unittest.TestCase().assertEqual(str(expect_code), str(actual_code), '校验接口返回码 预期返回码:%s 实际返回码:%s' % (str(expect_code),str(actual_code)))
    else:
        unittest.TestCase().assertNotEqual("0", str(actual_code),'校验接口返回码 预期返回码:非0 实际返回码:%s' % str(actual_code))

def check_keyword(ret,keyword):
    return ret.find(keyword)

def check_db(check_sql):
    check_sql_list = check_sql.split(';')
    for i in check_sql_list:
        if i:
            j = i.split('|')
            if j:
                sql = j[0]
                value = j[1]
                mysql = db.mysql()
                db_value = mysql.query(sql)
                unittest.TestCase().assertEqual(value,str(db_value),'校验数据库 sql:%s 预期值:%s 数据库中值:%s' %(sql,value,db_value))


if __name__ == '__main__':
    check_db("select count(*) from lambda.sys_branch where branch_name='test'|1;select count(*) from lambda.sys_branch where branch_name='test'|1;")