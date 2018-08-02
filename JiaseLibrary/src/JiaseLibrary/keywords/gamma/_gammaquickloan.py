
from robot.api import logger
import json




class _GammaQuickLoanKeywords():

    def __init__(self):
        pass

    def create_quick_cust(self,borrower_name=None,borrower_mobile=None):
        enterprise_name = self._faker.company()
        if borrower_mobile == None:
            borrower_mobile = self._faker.phone_number()
        owner_mobile = borrower_mobile
        borrower_id_code = self._faker.person_id()
        enterprise_code = self._faker.organization_code()
        url = '%s/gamma/cust/info/quick-loan/save' %self._gamma_url
        payloand ={
             "source": "MOBAI",
             "ownBusinessProperty": 'TRUE',
             "verified": 'FALSE',
             "cityName": "深圳市",
             "countyName": "南山区",
             "provinceName": "广东省",
             "street": "深南大道9789号",
             "provinceId": "440000",
             "cityId": "440300",
             "countryId": "440305",
             "countryName": "南山区",
             "businessAddress": "深南大道9789号",
             "enterpriseName": enterprise_name,
             "enterpriseCode":enterprise_code ,
             "ownerName": borrower_name,
             "borrowerName": borrower_name,
             "ownerMobile": owner_mobile,
             "borrowerMobile": borrower_mobile,
             "borrowerIdCode": borrower_id_code,
             "businessCategory": "CUST_PRODUCT_SEED,CUST_PRODUCT_PESTICIDE"
        }
        res = self._request.post(url,headers = self._headers,data = json.dumps(payloand))
        ret = json.loads(res.content.decode())
        data = ret.get('data')
        statusCode = ret.get('statusCode')
        statusDesc = ret.get('statusDesc')
        if statusCode == '0':
            logger.info('新建快捷贷客户:%s ,登录号:%s 成功' %(borrower_name,borrower_mobile))
            print('新建快捷贷客户:%s ,登录号:%s 成功' %(borrower_name,borrower_mobile))
            return data
        else:
            raise AssertionError('新建快捷贷客户失败，错误码：%s,错误信息：'%(statusCode,statusDesc))


