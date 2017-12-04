 # -*- coding:utf-8 -*-
import json
import hashlib
from robot.api import logger

class _LambdaSysOrganizeKeywords():
 
    # 系统管理组织架构相关的关键字,主要包括如下:机构管理,部门管理,岗位管理,角色管理
    # 组织架构比较固定,封装相应发方法主要是供其他模块查询调用
 
    def __init__(self):      
        self._lambda_url         = None
        self._lambda_all_psd     = None
        self._lambda_super_admin = None

    # 根据机构名称查询机构id
    def _query_branch_id(self,branch_name):
        url = '%s/sys/branchs/tree' %self._lambda_url
        params = {}
        res = self._request.get(url,headers=self._headers)
        response = res.content.decode('utf-8')
        for i in json.loads(response).get('data'):
            if i.get('name') == branch_name:
                return i.get('id')           
            
    # 根据部门名称查询部门id
    def _query_dept_id(self,branch_id,dept_name):
        url = '%s/sys/orgs/viewDept' %self._lambda_url
        params =    {
                    "branchId":branch_id
                    }
        res = self._request.get(url,params=params,headers=self._headers)
        response = res.content.decode('utf-8')
        for i in json.loads(response).get('data'):
            if i.get('deptName') == dept_name:
                return i.get('deptId')
    
    
    # 根据岗位名称查询岗位id
    def _query_position_id(self,branch_id,position_name):
        url = '%s/sys/position/list/filter/branch_id' %self._lambda_url
        params =    {
                    "branchId":branch_id
                    }
        res = self._request.get(url,params=params,headers=self._headers)
        response = res.content.decode('utf-8')
        for i in json.loads(response).get('list'):
            if i.get('positionName') == position_name:
                return i.get('positionId')
    
    # 根据角色名称查询角色id
    def _query_role_id(self,dept_id,role_name):
        url = '%s/sys/roles/dept_role_list' %self._lambda_url
        params =    {
                    "deptId":dept_id
                    }
        res = self._request.get(url,params=params,headers=self._headers)
        response = res.content.decode('utf-8')
        for i in json.loads(response).get('data'):
            if i.get('roleName') == role_name:
                return i.get('id')
    
    
                    
         
        
        
        
        
