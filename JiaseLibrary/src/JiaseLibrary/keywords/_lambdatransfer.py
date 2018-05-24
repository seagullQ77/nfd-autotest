# -*- coding:utf-8 -*-
import json
from robot.api import logger
from JiaseLibrary.utils.http import check_json_response

class _LambdaTransferKeywords():
    """
    移交管理
    """

    def transfer_manager(self, cust_name, cust_manager_name, new_cust_manager_name):
        """
        管户经理变更
        :return:
        http://lambda-web-test.ronaldinho.svc.cluster.local/transfer/cust/manager/record/updateCustManager
        """

        # 查询管户经理
        old_cust_manager_name, old_cust_manager_id, old_cust_manager_orgid = self.get_cust_manager(cust_manager_name)
        cust = self.cust_infos_queryByName(cust_name)
        cust_id = cust['id']
        new_cust_manager_name, new_cust_manager_id, new_cust_manager_orgid = self.get_cust_manager(new_cust_manager_name)
        params = {
            "custIds":cust_id,
            "oldCustManagerId": old_cust_manager_id,
            "oldCustOrgId": old_cust_manager_orgid,
            "newCustManagerId": new_cust_manager_id,
            "newCustOrgId":new_cust_manager_orgid,
        }
        url = '%s/transfer/cust/manager/record/updateCustManager' % self._lambda_url
        res = self._request.post(url, data = params)
        ret = check_json_response(res)



    def get_cust_manager(self, name):
        """
        查询管户经理
        :param name:
        :return:

        "http://lambda-web-test.ronaldinho.svc.cluster.local/transfer/cust/manager/record/selectCustManager?_ukey=5381&r=0.13963574590581307&custManagerName=admin"
        """
        params = {
            "custManagerName": name,
        }
        url = '%s/transfer/cust/manager/record/selectCustManager' % self._lambda_url
        res = self._request.get(url, params=params)
        ret = check_json_response(res)
        if len(ret['data']) == 0:
            raise AssertionError("没有找到名为 %s 的管户经理 ！" % name)
        elif len(ret['data']) > 1:
            logger.warn("%s 对应不止一个管户经理，暂时只选择第一个！")
        c = ret['data'][0]
        return c['custManagerName'], c['custManagerId'], c['custOrgId']


