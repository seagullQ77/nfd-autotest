from _lambdasysauth import _LambdaSysAuthKeywords
import json


class _LambdaReuseIOUKeywords():
    def __init__(self):
        pass


    def delLendL(self,lend_code):
        """
        删除借据
        :param self:
        :param lend_code:
        :return:
        """

        url = '%s/lendMock/delLendL' % self._delta_port
        params = {
            "lendCode": lend_code,
            "flag":'ALL'
        }
        res = self._request.get(url, params=params)
        response = res.content.decode('utf-8')
        status = json.loads(response).get('statusCode')
        statusDesc = json.loads(response).get('statusDesc')
        if status == '0':
           print(statusDesc)
        else:
            raise AssertionError( statusDesc)

    def syncIou2Delta(self,lend_code):
        """
        重新同步到delta
        :param self:
        :param lend_code:
        :return:
        """
        self.login_lambda(role='lambda_audit_1')
        url = '%s/repayment/query/syncIou2Delta' % self._lambda_server_port
        params = {
            "iouCode": lend_code
        }
        res = self._request.get(url, params=params)
        response = res.content.decode('utf-8')
        status = json.loads(response).get('statusCode')
        statusDesc = json.loads(response).get('statusDesc')
        if status == '0':
           print(statusDesc)
        else:
            raise AssertionError( statusDesc)

    def p2pValueDate(self, lend_code,valu_date='2018/03/05'):
        """
        p2p满标同步lambda待放款
        :param self:
        :param lend_code
        :param valu_date
        :return:
        """
        self.login_lambda(role='lambda_audit_1')
        url = '%s/sysmock/p2pValueDate' % self._lambda_server_port
        params = {
            "iouCode": lend_code,
            "valueDate":valu_date,
            "iouStatus":'DFK'
        }
        res = self._request.get(url, params=params)
        response = res.content.decode('utf-8')
        result = json.loads(response)
        if result == 'SUCCESS':
            print(result)
        else:
            raise AssertionError(result)

    def betaPayDone(self,lend_code,beta_pay_date= None):
        """
        模拟放款成功
        :param self:
        :param lend_code
        :param beta_pay_date
        :return:
        """
        url = '%s/lendMock/betaPayDone' % self._delta_url
        params = {
            "lendCode": lend_code,
            "betaPayDate":beta_pay_date
        }
        res = self._request.get(url, params=params)
        response = res.content.decode('utf-8')
        status = json.loads(response).get('statusCode')
        statusDesc = json.loads(response).get('statusDesc')
        if status == '0':
            print(statusDesc)
        else:
            raise AssertionError(statusDesc)


    def reuseIOU(self,lend_code):
        #删除借据
        self.delLendL(lend_code)
        #重新同步到delta
        self.syncIou2Delta(lend_code)
        #待放款
        self.p2pValueDate(lend_code)
        #放款成功
        self.betaPayDone(lend_code)









