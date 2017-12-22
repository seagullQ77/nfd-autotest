 # -*- coding:utf-8 -*-
import json
import hashlib
from robot.api import logger
from warnings import catch_warnings
from utils.lambda_db import LambdaDbCon

class _LambdaSysUserKeywords():
    
    
    def __init__(self):      
        self._lambda_url        = None
        self._lambda_all_psd     = None
        self._lambda_super_admin = None

    def _add_user(self,account=None,real_name=None,branch_id=None):
        url = '%s/sys/users/create' %self._lambda_url
        if account is None:
            account = self._faker.phone_number()
        if real_name is None:
            real_name = self._faker.name()
        if branch_id is None:
            branch_id = self._faker.phone_number()    
        staff_id = str(self._faker.random_int(1000,9999))    
        id_card_no = self._faker.person_id()
        if int(id_card_no[16])%2 == 0:
            sex= 'F'
        else:
            sex = 'M'
        payload =   {
                    "staffId":staff_id,
                    "realName":real_name,
                    "mobilePhone":account,
                    "sex":sex,
                    "idCardNo":id_card_no,
                    "userStatus":"NORMAL",
                    "wechatId":"test",
                    "email":"test@test",
                    "userDesc":"",
                    "branchId":branch_id,
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
        password = id_card_no[-4:] + staff_id
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
            
    def add_lambda_user(self,account=None,real_name=None,branch_name=None,
                        dept_name=None,position_name=None,role_name=None):
        branch_id = self._query_branch_id(branch_name)
        user_info = self._add_user(account,real_name,branch_id)
        account = user_info[1]
        dept_id = self._query_dept_id(branch_id, dept_name)
        position_id = self._query_position_id(branch_id, position_name)
        role_id = self._query_role_id(dept_id, role_name)
    
        url = '%s/sys/users/insert_position_roles' %self._lambda_url    
        payload =   {
                    "userId":user_info[0],
                    "roleIds":role_id,
                    "positionIds":position_id,
                    "deptId":dept_id,
                    "branchId":branch_id
                    }
        res = self._request.post(url,data=payload)
        status = json.loads(res.content.decode('utf-8')).get('statusCode')
        if status == '0':
            logger.info(u'新增用户明细成功:%s' %account) 
            self._update_user_password_by_db(account)        
        else:
            logger.error(u'新增用户明细失败:%s' %account) 
            raise AssertionError(u'新增用户明细失败:%s' %account)
                    
    


