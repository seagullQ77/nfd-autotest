import hashlib
import json
from robot.api import logger

class _GammaSysAuthKeywords():

    def __init__(self):
        pass

    def login_gamma(self,role=None,usr=None,psd=None):
        #self.logout_gamma()
        if usr is None:
            if role is not None:
                if hasattr(self, '_%s'%role):
                    usr = getattr(self,'_%s'%role)
                else:
                    logger.error('Role: %s not defined in config.cfg,please check again' %role)
                    raise AssertionError('Role: %s not defined in config.cfg,please check again' %role)
            else:
                usr=self._gamma_invest_manager
        if psd is None:
            psd = self._gamma_all_psd
        psd = hashlib.sha256(psd.encode()).hexdigest()

        url = '%s/gamma/auth/login' %self._gamma_url
        payload = {
            "username":usr,
            "password":psd
        }
        res = self._request.post(url=url,headers = self._headers,data = json.dumps(payload))
        ret = json.loads(res.content.decode())
        status = ret.get('statusCode')
        statusDesc = ret.get('statusDesc')
        data = ret.get('data')
        if status == '0':
            logger.info('登陆成功')
            print('登陆成功')
            return data
        else:
            raise AssertionError('登陆失败,错误码:%s,错误信息:%s' % (status, statusDesc))

    def logout_gamma(self):
        url = '%s/gamma/auth/logout' %self._gamma_url
        res = self._request.post(url,headers = self._headers)
        ret = json.loads(res.content.decode())
        statusCode = ret.get('statusCode')
        statusDesc = ret.get('statusDesc')
        if statusCode == '0':
            logger.info('退出当前用户')
            print('退出当前用户')
        else:
            raise AssertionError('退出展业端失败，错误码：%s，错误信息：%s'%(statusCode,statusDesc))
