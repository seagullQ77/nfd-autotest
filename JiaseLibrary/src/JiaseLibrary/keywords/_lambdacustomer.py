 # -*- coding:utf-8 -*-
import json
from robot.api import logger

class _LambdaCustomerKeywords():
    
    def __init__(self):        
        pass
    
    '''
          新增客户
    custKind:客户类型，若不传，则默认都选择,参数类型:'HZS|DBKH|DKKH' 代表 '合作商|担保客户|贷款客户' 
    custName:客户姓名,若不传,则随机生成
    idCode:客户身份证号,若不传,则随机生成   
    '''   
    def add_custom_personal(self,custKind=None,custName=None,idCode=None):
        url = '%s/cust/infos/personal/create' % self._lambda_url
        if custName is None:
            custName = self._faker.name_wuxia()
        if idCode is None:
            idCode = self._faker.person_id()
            
        cust_list = []
        cust_kind = ''
        if custKind is None:
            cust_kind = '1,2,4'
        else:
            custKind = custKind.split('|')
            if 'DKKH' in custKind :
              cust_list.append('1')
            if 'DBKH' in custKind :
              cust_list.append('2')
            if 'HZS' in custKind :
              cust_list.append('4')
        cust_kind = ','.join(cust_list)
            
        payload =   {
                    "baseInfo":     {
                                    "custName":custName,
                                    "custKind":cust_kind,
                                    "idType":'GR_SFZ',
                                    "idCode":idCode,
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
            logger.info(u'新增个人客户成功:%s' %custName)
        else:
            raise AssertionError(u'新增个人客户失败:%s' %custName)