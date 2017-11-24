#!/usr/bin/env python3
#coding=utf-8

import json
import hashlib
import requests

headers =   {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            "Content-Type": "application/json"
            }
def login(host,username,password=None,branchName=None,deptName=None):
    if not password:
        password = '150315'
    password = hashlib.sha256(password.encode()).hexdigest()
    url = 'http://%s/auth/login' % host
    payload =   {
                "username":username,
                "password":password
                }
    res = requests.post(url,headers=headers,data=json.dumps(payload))

    ret = json.loads(res.content.decode())
    if ret.get('statusCode') == '0':
        if branchName  and deptName:
            data = ret.get('data')
            for i in data:
                if i.get('branchName')==branchName and i.get('deptName')==deptName:
                    orgId = i.get('orgId')
                    branchId = i.get('branchId')
                    break
        else:
            orgId = ret.get('data')[0].get('orgId')
            branchId = ret.get('data')[0].get('branchId')

        if 'orgId' not in locals().keys():
            print('组织不存在,机构%s不存在或者部门%s不存在' %(branchName,deptName))

    else:
        print('登录失败,错误码:%s,错误信息:%s' %(ret.get('statusCode'),ret.get('statusDesc')))

    url = 'http://%s/auth/switchOrg' % host
    payload =   {
                "username":username,
                "password":password,
                "orgId":orgId
                }
    res = requests.post(url,headers=headers,data=json.dumps(payload))
    ret = json.loads(res.content.decode())
    if ret.get('statusCode') == '0':
        token = ret.get('data').get('token')
    else:
        print('选择机构失败,错误码:%s,错误信息:%s' %(ret.get('statusCode'),ret.get('statusDesc')))
    return token,branchId,orgId

if __name__ == '__main__':
    host='10.1.60.54'
    print(login(host,'13570927312', '150315'))
    login(host,'13570927312', '150315','华东区1','市场部')