from JiaseLibrary.utils.http import check_json_response


class _PaltformKeywords():

    def create_funds_account(self):
        """
        开通资金存管账户
        :return:
        """

        ret = self.cust_platform_accout_getAccountList()
        custId = ret['data'][0]['custId']
        ret = self.cust_platform_accout_add_init(custId)
        idCardNo = ret['data']['idCardNo']


        aaa = 1



    def cust_platform_accout_add_init(self, custId):
        """
        绑卡初始化
        :return:
        """
        url = "%s/cust/platform/accout/add/init" % self.interface_url
        load = {
            "custId": custId,
            "userRole": "BORROWERS",
        }
        resp = self.session.get(url, params = load)
        ret = check_json_response(resp)
        return ret

    def cust_platform_accout_getAccountList(self):
        """
        存管账户列表页
        :return:
        """
        url = "%s/cust/platform/accout/getAccountList" % self.interface_url
        load = {
        }

        resp = self.session.get(url, params = load)
        ret = check_json_response(resp)
        return ret

    def custInfo_platform_person_add(self):
        pass
