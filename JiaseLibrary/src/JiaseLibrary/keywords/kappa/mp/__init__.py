import requests
from robot.api import logger
from urllib import parse
import json
from JiaseLibrary.version import VERSION
from JiaseLibrary.keywords.kappa.mp.sys import _SysKeywords
from JiaseLibrary.keywords.kappa.mp.platform import _PaltformKeywords

from JiaseLibrary.utils.http import check_json_response

__version__ = VERSION


class KappaMpLibrary(
    _SysKeywords
    , _PaltformKeywords
):
    """
    kappa-mp 相关的关键字

    """

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    ROBOT_SUPPRESS_NAME = False
    ROBOT_EXIT_ON_FAILURE = True

    def __init__(self
                 , host="127.0.0.1"
                 , port="8011"):
        """

        :param host: 指定kappa-backend-mp的地址
        :param port: 指定kappa-backend-mp的端口
        """
        super(KappaMpLibrary, self).__init__()

        self._host = host
        self._port = port
        self.interface_url = "http://%s:%s" % (self._host, self._port)

        self.session = requests.session()
        self.session.headers["Content-Type"] = "application/json"

    # High-Leverl的关键字先放这里吧，包里面放对应的后台的接口

    def create_funds_account(self, bankcardNo, mobile, password = "123456"):
        """
        开通资金存管账户
        :return:
        """

        ret = self.cust_platform_accout_getAccountList()
        # 获取 custId
        custId = ret['data'][0]['custId']
        realName = ret['data'][0]['name']
        ret = self.cust_platform_accout_add_init(custId)

        idCardNo = ret['data']['idCardNo']
        authList = [x['value'] for x in ret['data']['authList']]
        ret = self.custInfo_platform_person_add(realName, idCardNo, authList, custId)
        lanmaoly_param = ret['data']['data'].copy()
        del lanmaoly_param['reqDataObj']
        lanmaoly_url = ret['data']['url']
        j = json.loads(ret['data']['data']['reqData'])
        credType = j['idCardType']
        userRole = j['userRole']
        requestNo = j['requestNo']
        platformUserNo = j['platformUserNo']

        headers = self.session.headers.copy()
        headers['Content-Type'] = "application/x-www-form-urlencoded"
        headers['Host'] = "hubk.lanmaoly.com"
        headers['Accept'] = "application/json, text/javascript, */*; q=0.01"

        resp = self.session.post(lanmaoly_url, data=lanmaoly_param, headers=headers)
        assert resp.status_code == 200
        query = parse.parse_qs(parse.urlparse(resp.url)[4])
        requestKey = query['requestKey'][0]

        # 检查银行卡
        load = {
            "bankcardNo": bankcardNo,
            "requestKey": requestKey,
            "serviceType": "BANKCARD_AUTH",
        }

        resp = self.session.post(parse.urljoin(resp.url,"/bha-neo-app/gateway/bankcard/bin"), data=load, headers = headers)
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
        resp = self.session.post(parse.urljoin(resp.url, "/bha-neo-app/gateway/sms/smsForEnterprise"), data=load,headers=headers)
        assert resp.status_code == 200
        assert json.loads(resp.text)['status'] == "SUCCESS"
        logger.info(json.loads(resp.text)['message'])

        # 提交注册
        load = {
            "serviceType": "BANKCARD_AUTH",
            "realName": realName,
            "credType": credType,
            "idCardNo" : idCardNo,
            "maskedCredNum" : "" ,
            "bankcardNo" : bankcardNo,
            "mobile" : mobile,
            "smsCode" : 150315,
            "password" : password,
            "confirmPassword" : password,
            #"protocolCheckBox" : "false",
            "requestKey" : requestKey,

        }

        headers_html = headers.copy()
        headers_html['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        resp = self.session.post(parse.urljoin(resp.url, "/bha-neo-app/gateway/mobile/personalRegisterExpand/register"), data=load, headers=headers_html)
        assert resp.status_code == 200
        return ret
