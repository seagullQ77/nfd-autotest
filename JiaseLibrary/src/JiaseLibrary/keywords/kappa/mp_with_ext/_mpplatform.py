from robot.api import logger
from urllib import parse
import json
from JiaseLibrary.utils.http import check_json_response


class _MpPaltformKeywords():

    def _cust_platform_accout_add_init(self, custId, userRole = "BORROWERS"):
        """
        绑卡初始化
        :return:
        """
        url = "%s/cust/platform/accout/add/init" % self.interface_url
        load = {
            "custId": custId,
            "userRole": userRole,
        }
        resp = self.session.get(url, params = load)
        ret = check_json_response(resp)
        return ret

    def _cust_platform_accout_getAccountList(self):
        """
        存管账户列表页

        获取所有相关用户的借款账户，担保账户信息
        :return:
        """
        url = "%s/cust/platform/accout/getAccountList" % self.interface_url
        resp = self.session.get(url)
        ret = check_json_response(resp)
        print(ret)
        return ret

    def _custInfo_platform_person_add(self, realName, idCardNo, authList, custId, userRole="BORROWERS"):
        """
        个人借款账户绑卡
        :param realName:
        :param idCardNo:
        :param authList:
        :param custId:
        :return:
        """
        url = "%s/custInfo/platform/person/add" % self.interface_url

        load = {
            "realName": realName,
            "idCardNo": idCardNo,
            "authList" : authList,
            "custId" : custId,
            "userRole": userRole,
            "frontUrl" : None,
        }
        resp = self.session.post(url, json=load)
        ret = check_json_response(resp)
        return ret


    def create_funds_account_GR(self, userRole = None, bankcardNo = None, mobile = None, password = "123456"):
        """
        开通个人资金存管账户
        :return:
        """
        # GET http://kappa-mp-test.ronaldinho.svc.cluster.local/cust/platform/accout/add/init?_ukey=5381&r=0.2863182303018188&custId=31&userRole=GUARANTEECORP HTTP/1.1
        ret = self._cust_platform_accout_getAccountList()
        # 获取 custId
        custId = ret['data'][0]['custId']
        realName = ret['data'][0]['name']
        ret = self._cust_platform_accout_add_init(custId, userRole=userRole)

        idCardNo = ret['data']['idCardNo']
        authList = [x['value'] for x in ret['data']['authList']]
        ret = self._custInfo_platform_person_add(realName, idCardNo, authList, custId, userRole=userRole)
        lanmaoly_param = ret['data']['data'].copy()
        del lanmaoly_param['reqDataObj']
        lanmaoly_url = ret['data']['url']
        j = json.loads(ret['data']['data']['reqData'])
        credType = j['idCardType']

        headers = self.session.headers.copy()
        headers['Content-Type'] = "application/x-www-form-urlencoded"
        headers['Host'] = "hubk.lanmaoly.com"
        headers['Accept'] = "application/json, text/javascript, */*; q=0.01"

        resp = self.session.post(lanmaoly_url, data=lanmaoly_param, headers=headers)
        assert resp.status_code == 200
        query = parse.parse_qs(parse.urlparse(resp.url)[4])
        requestKey = query['requestKey'][0]

        if bankcardNo == None:
            bankcardNo = self._faker.credit_card_number()
        if mobile == None:
            mobile = self._faker.phone_number()

        # 检查银行卡
        load = {
            "bankcardNo": bankcardNo,
            "requestKey": requestKey,
            "serviceType": "BANKCARD_AUTH",
        }

        resp = self.session.post(parse.urljoin(resp.url, "/bha-neo-app/gateway/bankcard/bin"), data=load,
                                 headers=headers)
        assert resp.status_code == 200
        if json.loads(resp.text)['success'] != True:
            raise AssertionError("%s, 卡号：%s" % (json.loads(resp.text)['msg'], bankcardNo))
        logger.info(json.dumps(json.loads(resp.text)))

        # 获取验证码
        load = {
            "bizType": "REGISTER",
            "mobile": mobile,
            "requestKey": requestKey,
        }
        resp = self.session.post(parse.urljoin(resp.url, "/bha-neo-app/gateway/sms/smsForEnterprise"), data=load,
                                 headers=headers)
        assert resp.status_code == 200
        assert json.loads(resp.text)['status'] == "SUCCESS"
        logger.info(json.loads(resp.text)['message'])

        # 提交注册
        load = {
            "serviceType": "BANKCARD_AUTH",
            "realName": realName,
            "credType": credType,
            "idCardNo": idCardNo,
            "maskedCredNum": "",
            "bankcardNo": bankcardNo,
            "mobile": mobile,
            "smsCode": 150315,
            "password": password,
            "confirmPassword": password,
            # "protocolCheckBox" : "false",
            "requestKey": requestKey,

        }

        headers_html = headers.copy()
        headers_html['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        resp = self.session.post(parse.urljoin(resp.url, "/bha-neo-app/gateway/mobile/personalRegisterExpand/register"),
                                 data=load, headers=headers_html)
        print(resp.text)
        assert resp.status_code == 200
        return ret


    def _custInfo_platform_company_add(self, mobile, unifiedCode, authList, custId, userRole):
        """
        企业借款账户绑卡
        :param mobile:
        :param unifiedCode:
        :param authList:
        :param custId:
        :return:

        """
        url = "%s/custInfo/platform/company/add" % self.interface_url
        bankcardNo = self._faker.credit_card_number()
        contactName = self._faker.name()

        load = {

            "unifiedCode": unifiedCode,
            "bankcode": "FJIB",
            "bankcardNo": bankcardNo,
            "contactName": contactName,
            "mobile": mobile,
            "authList": authList,
            "custId": custId,
            "userRole": userRole,
            "bankName": "兴业银行",
            "frontUrl": None

        }
        resp = self.session.post(url, json=load)
        ret = check_json_response(resp)
        return ret

    def create_funds_account_QY(self, userRole = "BORROWERS", mobile = None):
        """
        企业开通资金存管账户
        userRole:GUARANTEECORP or  BORROWERS
        :return:
        """
        ret = self._cust_platform_accout_getAccountList()#获取custId
        custId = ret['data'][0]['custId']

        ret = self._cust_platform_accout_add_init(custId, userRole=userRole)
        unifiedCode = ret['data']['unifiedCode']
        authList = [x['value'] for x in ret['data']['authList']]

        ret = self._custInfo_platform_company_add(mobile, unifiedCode, authList, custId, userRole=userRole)
        lanmaoly_param = ret['data']['data'].copy()
        del lanmaoly_param['reqDataObj']
        lanmaoly_url = ret['data']['url']

        headers = self.session.headers.copy()
        headers['Content-Type'] = "application/x-www-form-urlencoded"
        headers['Host'] = "hubk.lanmaoly.com"
        headers['Accept'] = "application/json, text/javascript, */*; q=0.01"

        resp = self.session.post(lanmaoly_url, data=lanmaoly_param, headers=headers)
        assert resp.status_code == 200

        query = parse.parse_qs(parse.urlparse(resp.url)[4])
        requestKey = query['requestKey'][0]


        # 获取验证码
        load = {
            "bizType": "REGISTER",
            "requestKey": requestKey,
        }
        resp = self.session.post(parse.urljoin(resp.url, "/bha-neo-app/gateway/sms/sms"), data=load,
                                 headers=headers)

        assert resp.status_code == 200
        assert json.loads(resp.text)['status'] == "SUCCESS"
        logger.info(json.loads(resp.text)['message'])

        # 提交注册
        load = {
            "smsCode": 150315,
            "requestKey":requestKey,
            #"protocolCheckBox":'false',
            "password" : 150315,
            "confirmPassword":150315,
            "bankCode":'FJIB'
        }

        headers_html = headers.copy()
        headers_html['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        resp = self.session.post(parse.urljoin(resp.url, "/bha-neo-app/gateway/mobile/enterpriseRegister/registerEnterprise"),
                                 data=load, headers=headers_html)
        assert resp.status_code == 200
        return ret
        
        







