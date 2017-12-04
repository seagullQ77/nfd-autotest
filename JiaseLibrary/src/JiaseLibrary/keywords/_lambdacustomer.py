 # -*- coding:utf-8 -*-
import json
from robot.api import logger

class _LambdaCustomerKeywords():
    
    def __init__(self):        
        pass
    
 
    # 新增客户
    # cust_kind:客户类型，若不传，则默认都选择,参数类型:'HZS|DBKH|DKKH' 代表 '合作商|担保客户|贷款客户' 
    # cust_name:客户姓名,若不传,则随机生成
    # id_code:客户身份证号,若不传,则随机生成 
    # 返回:cust_id 客户id,在后面的授信管理、提款管理都会用到  
   
    def add_custom_personal(self,cust_kind=None,cust_name=None,id_code=None):
        url = '%s/cust/infos/personal/create' % self._lambda_url
        if cust_name is None:
            cust_name = self._faker.name_wuxia()
        if id_code is None:
            id_code = self._faker.person_id()
            
        cust_list = []
        cust_kind_str = ''
        if cust_kind is None:
            cust_kind_str = '1,2,4'
        else:
            cust_kind = cust_kind.split('|')
            if 'DKKH' in cust_kind :
              cust_list.append('1')
            if 'DBKH' in cust_kind :
              cust_list.append('2')
            if 'HZS' in cust_kind :
              cust_list.append('4')
        cust_kind_str = ','.join(cust_list)
            
        payload =   {
                    "baseInfo":     {
                                    "custName":cust_name,
                                    "custKind":cust_kind_str,
                                    "idType":'GR_SFZ',
                                    "idCode":id_code,
                                    "idExpire":"",
                                    "isLimitless":'',
                                    "createChannel":"20"
                                    },
                    "idExpire":"",
                    "isLimitless":"true"
                    }
        res = self._request.post(url,headers=self._headers,data=json.dumps(payload))
        status = json.loads(res.content.decode('utf-8')).get('statusCode')
        if status == '0':
            logger.info(u'新增个人客户成功:%s' %cust_name)
        else:
            raise AssertionError(u'新增个人客户失败:%s' %cust_name)
            
    # 补充个人客户的详细信息
    def _creat_custom_personal_detail(self,cust_id):    
        pass
        self._creat_cust_personal_business()
        self._creat_cust_personal_contact()
        
    # 补充个人客户的经营信息
    def _creat_cust_personal_business(self,cust_id):
        pass
    
    # 补充个人客户的联系人信息
    def _creat_cust_personal_contact(self,cust_id):
        pass
    
    # 新增企业客户
    # cust_kind:客户类型，若不传，则默认都选择,参数类型:'HZS|DBKH|DKKH' 代表 '合作商|担保客户|贷款客户' 
    # cust_name:企业名称,若不传,则随机生成
    # id_type:企业证件类型,营业执照号或者社会信用码,若不传则默认使用社会信用码
    # id_code:证件号码,若不传,则随机生成 
    # 返回:cust_id 客户id,在后面的授信管理、提款管理都会用到  
    def add_cust_enterprise(self,cust_kind=None,cust_name=None,id_type=None,id_code=None):
        return cust_id
            
    # 通过cust id获取客户详细信息
    # 返回字典对象
    # {'cust_name':'zhangsan','cust_type':'GR','id_type':'SFZ','id_no':'440111197203175846'}
    def _get_cust_info_by_id(self,cust_id):
       return {}
        
    
    
    
    
    
    