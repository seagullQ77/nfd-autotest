import requests
import os
import configparser
from faker.factory import Factory
from JiaseLibrary.version import VERSION
from JiaseLibrary.keywords.kappa.mp_with_ext._mpsys import _MpSysKeywords
from JiaseLibrary.keywords.kappa.mp_with_ext._mpplatform import _MpPaltformKeywords


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
CONF_PATH = BASE_DIR  + "\\config\\config.cfg"
print(CONF_PATH)


__version__ = VERSION


class KappaMpLibrary(
    _MpSysKeywords
    , _MpPaltformKeywords
):
    """
    kappa-mp 相关的关键字

    """

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    ROBOT_SUPPRESS_NAME = False
    ROBOT_EXIT_ON_FAILURE = True

    def __init__(self, host=None, port=None ,source = None):
        self._host = host
        self._port = port
        self._faker = Factory.create(locale='zh_CN')
        self._get_config(source)

    def _get_config(self,source = None):

        cf = configparser.ConfigParser()
        cf.read(CONF_PATH, encoding='utf-8')
        if source == 'ext':
            self._kappa_mp_ext_host = self._host or cf.get('kappa_mp_ext', 'kappa_mp_ext_host')
            self._kappa_mp_ext_port = self._port or cf.get('kappa_mp_ext', 'kappa_mp_ext_port')
        else:
            self._kappa_mp_host = self._host or cf.get('kappa_mp', 'kappa_mp_host')
            self._kappa_mp_port = self._port or cf.get('kappa_mp', 'kappa_mp_port')

        self.interface_url = "http://%s" % (self._kappa_mp_host)
        print(self.interface_url)

        self.session = requests.session()
        self.session.headers["Content-Type"] = "application/json"
        print(self.session.headers)




if __name__ == '__main__':
     jiaseMP = KappaMpLibrary(source='ext')
     jiaseMP.login_with_sms(18777777777,150315)
     jiaseMP.submit_register(18777777777)
     jiaseMP.create_funds_account_GR(mobile=18777777777,userRole = "GUARANTEECORP")
     #jiaseMP.create_funds_account_QY(mobile=18888888885,userRole = "BORROWERS")









