# -*- coding:utf-8 -*-
import json
from robot.api import logger
from JiaseLibrary.utils.http import check_json_response

class _LambdaProductKeywords():
    """
    对应菜单的产品管理
    """

    def create_product(self, name1, name2, name3, remark, accountingBelonging, displayable, custType, accountingSubjectDes):
        """
        创建产品
        :return:
        """
        # 查询已有的产品树
        tree = self.prod_childproduct_displayable_tree()
        # 找一级产品
        level1_product = [x for x in tree['data'] if x['pId'] == 0]
        p = [x for x in level1_product if x['name'] == name1]
        assert len(p) > 0, "没有找到一级产品 %s" % name1
        p = p[0]
        p1id = p['id']

        p2 = [x for x in tree['data'] if x['name'] == name2 and x['pId'] == p1id]
        if name3 == "X":
            # 创建二级产品
            if len(p2) > 0:
                logger.info("已经存在名为 %s 的产品了！" % name2)
                return False
            else:
                pid = p1id
                name = name2
        else:
            # 创建三级产品
            if len(p2) == 0:
                raise AssertionError("没有找到二级产品 %s" % name2)
            else:
                p2 = p2[0]
                p2id = p2['id']
                p3 = [x for x in tree['data'] if x['name'] == name3 and x['pId'] == p2id]
                if len(p3) > 0:
                    logger.info("已经存在名为 %s 的产品了！" % name3)
                    return False

                pid = p2['id']
                name = name3
        params = {
            "id":pid,
            "name":name,
            "displayable":displayable,
            "accountingBelonging":accountingBelonging,
            "custType":custType,
            # 暂时直接结算主体为农金圈
            "accountingSubject":"1",
            "accountingSubjectDes":"农金圈",
            "remark":remark,
        }
        url = '%s/prod/childproduct/create' % self._lambda_url
        res = self._request.post(url, json = params)
        ret = check_json_response(res)

    def create_product2(self, pname,name, remark = None, accountingBelonging = "BN", displayable = "true", custType = "GR,QY", accountingSubjectDes = "农金圈"):
        """
        创建二级产品
        :return:
        """
        return self.create_product(pname,name,"X", remark,accountingBelonging, displayable, custType, accountingBelonging)

    def create_product3(self, pname1,pname2, name, remark = None, accountingBelonging = "BN", displayable = "true", custType = "GR,QY", accountingSubjectDes = "农金圈"):
        """
        创建三级产品
        :return:
        """
        return self.create_product(pname1, pname2, name, remark, accountingBelonging, displayable, custType, accountingBelonging)


    def prod_childproduct_displayable_tree(self):
        """
        GET /prod/childproduct/displayable_tree
        获取需要展示的产品树
        :return:
        """
        url = '%s/prod/childproduct/displayable_tree' % self._lambda_url
        res = self._request.get(url,)
        ret = check_json_response(res)
        return ret
