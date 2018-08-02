
from JiaseLibrary.version import VERSION
import os
import requests
import configparser
from JiaseLibrary.keywords.gamma._gammasysauth import _GammaSysAuthKeywords
from JiaseLibrary.keywords.gamma._gammaquickloan import _GammaQuickLoanKeywords
from faker.factory import Factory
from faker_nfd import NfdCompanyProvider
# from faker import Faker


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CONF_PATH = BASE_DIR  + "\\config\\config.cfg"


class GammaLibrary(_GammaSysAuthKeywords,_GammaQuickLoanKeywords):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION


    def __init__(self,gamma_host=None,gamma_port=None):
        self.gamma_host = gamma_host
        self.gamma_port = gamma_port
        self._init_request_arg()
        self._get_config()
        self._init_request_arg()

        self._faker   = Factory.create(locale='zh_CN')
        self._faker.add_provider(NfdCompanyProvider)

        #不能用，待查
        # self.faker = Faker("zh_cn")
        # self.faker.add_provider(NfdCompanyProvider)

    def _get_config(self):
        cf = configparser.ConfigParser()
        cf.read(CONF_PATH, encoding='utf-8')
        self._gamma_host = self.gamma_host or cf.get('gamma', 'gamma_host')
        self._gamma_port = self.gamma_port or cf.get('gamma', 'gamma_port')
        self._gamma_url = 'http://%s:%s' % (self._gamma_host, self._gamma_port)

        self._gamma_all_psd = cf.get('gamma_roles', 'gamma_all_psd')
        self._gamma_invest_manager = cf.get('gamma_roles', 'gamma_invest_manager')

    def _init_request_arg(self):
        self._request = requests.session()
        self._headers = {"Content-Type": "application/json"}



if __name__ == '__main__':

    jiaseG = GammaLibrary()
    jiaseG.login_gamma(role='gamma_invest_manager')
    jiaseG.create_quick_cust('test-快捷贷8','15500000008')
    #jiaseG.logout_gamma()