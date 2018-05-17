from JiaseLibrary.utils.http import check_json_response


class _PaltformKeywords():

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

        获取所有相关用户的借款，担保账户信息
        :return:
        """
        url = "%s/cust/platform/accout/getAccountList" % self.interface_url
        load = {
        }

        resp = self.session.get(url, params = load)
        ret = check_json_response(resp)
        return ret

    def custInfo_platform_person_add(self, realName, idCardNo, authList, custId):
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
            "userRole": "BORROWERS",
            "frontUrl" : None,
        }
        resp = self.session.post(url, json=load)
        ret = check_json_response(resp)
        return ret

