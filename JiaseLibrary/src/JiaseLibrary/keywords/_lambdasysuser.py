 # -*- coding:utf-8 -*-
import json
import hashlib
from robot.api import logger
from warnings import catch_warnings
from JiaseLibrary.utils.lambda_db import LambdaDbCon

class _LambdaSysUserKeywords():
    
    
    def __init__(self):      
        self._lambda_url        = None
        self._lambda_all_psd     = None
        self._lambda_super_admin = None

    def _add_user(self,account=None,realName=None,branchId=None):
        url = '%s/sys/users/create' %self._lambda_url
        if account is None:
            account = self._faker.phone_number()
        if realName is None:
            realName = self._faker.name()
        if branchId is None:
            branchId = self._faker.phone_number()    
        staffId = str(self._faker.random_int(1000,9999))    
        idCardNo = self._faker.person_id()
        if int(idCardNo[16])%2 == 0:
            sex= 'F'
        else:
            sex = 'M'
        payload =   {
                    "staffId":staffId,
                    "realName":realName,
                    "mobilePhone":account,
                    "sex":sex,
                    "idCardNo":idCardNo,
                    "userStatus":"NORMAL",
                    "wechatId":"test",
                    "email":"test@test",
                    "userDesc":"",
                    "branchId":branchId,
                    "account":account,
                    "id":""
                    }
        res = self._request.post(url,headers=self._headers,data=json.dumps(payload))
        status = json.loads(res.content.decode('utf-8')).get('statusCode')
        if status == '0':
            logger.info(u'新增用户成功:%s' %account)           
        else:
            logger.error(u'新增用户失败:%s' %account)
            raise AssertionError(u'新增用户失败:%s' %account)
        
        user_id = json.loads(res.content.decode('utf-8')).get('data')
        password = idCardNo[-4:] + staffId
        return (user_id,account,password) 
    
    
    def update_user_password(self,account,old_password,new_password=None):
       
        url = '%s/sys/users/updatePassword' %self._lambda_url
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        if new_password is None:
            new_password = self._lambda_all_psd
        new_password_encrpt = hashlib.sha256(new_password.encode()).hexdigest()
        old_password_encrpt = hashlib.sha256(old_password.encode()).hexdigest()
        payload =   {
                    "newPassword":new_password_encrpt,
                    "newPassword2":new_password_encrpt,
                    "oldPassword":old_password_encrpt
                    }
        
        self.login_lambda(account,old_password)  
        res = self._request.post(url,data=payload,headers=headers)
        status = json.loads(res.content.decode('utf-8')).get('statusCode')
        if status == '0':
            logger.info(u'修改账号密码成功:%s' %account)
            return json.loads(res.content.decode('utf-8')).get('data')
        else:
            logger.error(u'修改账号密码失败:%s' %account)
            raise AssertionError(u'修改账号密码失败:%s' %account)
        
    
    '''添加用户
       account:登录账号,即手机号,为None则随机生成一个手机号
       branchId:所属机构id,为None则随机选择       
    '''     
            
    def _update_user_password_by_db(self,account):
       
        lam_db = LambdaDbCon(self._lambda_host)
        lam_db.update_sys_user_password(account)
        
    
    '''添加用户
       account:登录账号,即手机号,为None则随机生成一个手机号
       branchId:所属机构id,为None则随机选择       
    '''     
            
    def add_lambda_user(self,account=None,realName=None,branch_name=None,
                        dept_name=None,position_name=None,role_name=None):
        branchId = self._query_branchId(branch_name)
        userinfo = self._add_user(account,realName,branchId)
        account = userinfo[1]
        deptId = self._query_deptId(branchId, dept_name)
        positionId = self._query_positionId(branchId, position_name)
        roleId = self._query_roleId(deptId, role_name)
    
        url = '%s/sys/users/insert_position_roles' %self._lambda_url    
        payload =   {
                    "userId":userinfo[0],
                    "roleIds":roleId,
                    "positionIds":positionId,
                    "deptId":deptId,
                    "branchId":branchId
                    }
        res = self._request.post(url,data=payload)
        status = json.loads(res.content.decode('utf-8')).get('statusCode')
        if status == '0':
            logger.info(u'新增用户明细成功:%s' %account) 
            self._update_user_password_by_db(account)        
        else:
            logger.error(u'新增用户明细失败:%s' %account) 
            raise AssertionError(u'新增用户明细失败:%s' %account)
                    
    


