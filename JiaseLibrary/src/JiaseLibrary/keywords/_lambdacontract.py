 # -*- coding:utf-8 -*-
import json
from robot.api import logger
import requests

class _LambdaContractKeywords():
    
    def __init__(self):
        self._lambda_url= None

    # 合同签订
    # loan_id 贷款申请的id,需要根据贷款申请id查询到对应的合同id
    def _query_con_id(self,loan_id):
        url = '%s/contract/main/list' % self._lambda_url
        params = {"loan_id": loan_id}
        res = self._request.get(url,params=params)
        response = res.content.decode('utf-8')
        for i in json.loads(response).get('list'):
            for key,value in i.items():
                if key == 'loanApplyId' and value == loan_id:
                    return i.get('id'),i.get('signStatus'),i.get('contractNo'),i.get('custName')


    def sign_loan_contract(self,loan_id=None):
        con_info = self._query_con_id(loan_id)
        #print (con_info)
        if con_info[1] == 'YQD':
            #print('%s合同已签订'%con_info[3])
            logger.info('%s合同已签订'%con_info[3])
        else:
            url = '%s/contract/main/sign' % self._lambda_url
            payload = {
                "id": con_info[0],
                "signStatus": "YQD"
            }
            res = self._request.post(url, headers=self._headers, data=json.dumps(payload))
            status = json.loads(res.content.decode('utf-8')).get('statusCode')
            statusDesc = json.loads(res.content.decode('utf-8')).get('statusDesc')
            if status == '0':
                #print('%s合同签约成功'%con_info[3])
                logger.info('%s合同签约成功'%con_info[3])
            else:
                #print(statusDesc + '——%s合同签约失败'%con_info[3])
                logger.error('%s合同签约失败——'%con_info[3]+statusDesc)
                #raise AssertionError('合同签约失败——%s' % statusDesc)




