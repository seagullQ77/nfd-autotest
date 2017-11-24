#!/usr/bin/env python3
#coding=utf-8

import json
import unittest
import requests
from public import login
from public import conf
from public import check

class MyTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def action(self,case):
        headers =   {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
                    "Content-Type": "application/json"
                    }

        method = case.get('Method')
        params = case.get('Params')
        expect_code = case.get('ExpectCode')
        description = case.get('Description')
        user = case.get('LoginUser')
        url = case.get('Connect')
        check_sql = case.get('Check_Sql').strip('\n')
        ip = conf.get_conf('server','ip')
        user_dict = conf.get_conf('user','user_dict')
        account = json.loads(user_dict).get(user)

        url = 'http://%s%s' %(ip,url)
        user_info = login.login(ip,account)
        token = user_info[0]
        cookies = {'token':token}
        params = json.loads(params)
        if method == 'get':
            res = requests.get(url,params=params,headers=headers,cookies=cookies)
        elif method == 'post':
            res = requests.post(url,data=json.dumps(params),headers=headers,cookies=cookies)

        ret = res.content.decode()
        elapsed_time = res.elapsed.total_seconds()
        print('用例描述:%s' % description)
        print('接口地址:%s' % url)
        print('输入:%s' % params)
        print('输出:%s' % ret)
        print('耗时:%s s' % elapsed_time)

        #校验返回码
        check.check_code(ret,expect_code)

        #校验数据库
        check.check_db(check_sql)

    @staticmethod
    def get_test_func(case):
        def func(self):
            self.action(case)
        return func

if __name__ == '__main__':
    unittest.main(defaultTest='MyTestCase')