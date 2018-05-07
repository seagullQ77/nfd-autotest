 # -*- coding:utf-8 -*-
import json
import hashlib
from robot.api import logger

class _LambdaSysAuthKeywords():
    
    
    def __init__(self):
        self._lambda_url        = None
        self._lambda_all_psd     = None
        self._lambda_super_admin = None

    '''系统鉴权,登录Lambda系统
       role:用配置文件中的lambda 角色登录,传入参数:lambda_invest_manager,role 不为None时,usr参数无效
       usr:登录用户名
       psd:用户名对应密码
       usr和role为None时，默认使用配置文件里的超级管理员登录
       usr为None，role不为None，读取配置文件中role对应账户登录
       usr不为None时直接使用usr传入的账户登录
       psd为None时，使用默认的密码，否则使用传入的值
    '''     
    def login_lambda(self,role=None,usr=None,psd=None):
        #登录前先退出当前登录用户
        self.logout_lambda()
        
        if usr is None:
            if role is not None:
                if hasattr(self, '_%s'%role):
                    usr = getattr(self,'_%s'%role)           
                else:
                    logger.error('Role: %s not defined in config.cfg,please check again' %role)
                    raise AssertionError('Role: %s not defined in config.cfg,please check again' %role)
            else:      
                usr=self._lambda_super_admin
        if psd is None:
            psd = self._lambda_all_psd
              
        psd = hashlib.sha256(psd.encode()).hexdigest()
  
        
        url = '%s/auth/login' % self._lambda_url
        payload =   {
                    "username":usr,
                    "password":psd
                    }
        res = self._request.post(url,headers=self._headers,data=json.dumps(payload))        
        
        res_content = json.loads(res.content.decode('utf-8'))
 
        res_data = res_content.get('data')
        status = res_content.get('statusCode')
        if status == 'SYS_408':
            return status
        
        if len(res_data) > 0:
            orgId = res_data[0].get('orgId')
            branchId = res_data[0].get('branchId')               
            url = '%s/auth/switchOrg' % self._lambda_url
            payload =   {
                        "username":usr,
                        "password":psd,
                        "orgId":orgId
                        }
            res = self._request.post(url,headers=self._headers,data=json.dumps(payload))
            status = json.loads(res.content.decode('utf-8')).get('statusCode')
            if status == '0':
                logger.info(u'登录lambda成功:%s'%usr)
            else:
                logger.error(u'登录lambda失败:%s'%usr)
                raise AssertionError(u'登录lambda失败:%s'%usr)
        else:
            logger.error(u'登录lambda失败:%s'%usr)
            raise AssertionError(u'登录lambda失败:%s'%usr)      
            
    '''
         当前用户退出lambda系统
    '''
    def logout_lambda(self):        
        url = '%s/auth/logout' %self._lambda_url
        headers = {"Accept": "application/json"}
        res = self._request.get(url,headers=headers)
        status = json.loads(res.content.decode('utf-8')).get('statusCode')
        if status != '0':
            raise AssertionError(u'退出lambda失败')
        else:
            logger.info(u'当前用户退出登录')
    
        
                   
                
                
        
        
        
        
    
    


