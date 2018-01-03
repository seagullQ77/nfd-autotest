 # -*- coding:utf-8 -*-
import json
from robot.api import logger

class _LambdaContractKeywords():
    
    def __init__(self):
        self._lambda_url= None


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

    # contract_no 根据合同编号返回对应的合同id(给提款用)
    def query_conid_by_contractno(self, contract_no):
        url = '%s/contract/main/list' % self._lambda_url
        params = {"loan_id": contract_no}
        res = self._request.get(url, params=params)
        response = res.content.decode('utf-8')
        for i in json.loads(response).get('list'):
            for key, value in i.items():
                if key == 'contractNo' and value == contract_no:
                    return i.get('id')

    #查询操作，确定签订后合同状态是否变为了已签订
    def _check_loan_contract_status(self, loan_id):
        con_info = self._query_con_id(loan_id)
        if con_info[1] == 'YQD':
            logger.info('%s合同签约成功,可继续申请提款' % con_info[3])
        else:
            logger.info('%s合同状态（%s）有误，签约失败,请查看原因——' %(con_info[3],con_info[1]))
            raise AssertionError('%s合同状态（%s）有误，签约失败,请查看原因——' %(con_info[3] %con_info[1]) )


    # 合同签订
    def sign_loan_contract(self,loan_id=None):
        con_info = self._query_con_id(loan_id)
        if con_info[1] == 'YQD':
            logger.info('%s合同已签订'%con_info[3])
            raise AssertionError('%s合同已签约，请检查流程是否正确' % con_info[3])
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
                self._check_loan_contract_status(loan_id)
            else:
                logger.error('%s合同签约失败——'%con_info[3]+statusDesc)
                raise AssertionError('%s合同签约失败——'%con_info[3]+statusDesc)











