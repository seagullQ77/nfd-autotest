import os
from keywords import *
from version import VERSION
import ConfigParser
from faker.factory import Factory

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONF_PATH = BASE_DIR  + "\\OmegaLibrary\\config\\config.conf"


__version__ = VERSION

class OmegaLibrary(
    _OmegaConsoleKeywords,
    _OmegaMpKeywords
):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self):        
        self._get_config_arg()
        self._browser = None
        self._omega_browser = None 
        self._mp_browser =None
        self._myfaker = Factory.create(locale='zh_CN')
        
    def _get_config_arg(self):
        cf = ConfigParser.ConfigParser()
        cf.read(CONF_PATH)
        self._omega_url=cf.get('omega','omega_url')
        self._omega_usr=cf.get('omega','omega_usr')
        self._omega_psd=cf.get('omega','omega_psd')
        self.omega_usr_name=cf.get('omega','omega_usr_name')
        self.omega_usr_no=cf.get('omega','omega_usr_no')
        self._browser_type=cf.get('omega','browser')
        
        self._mp_ord_url = cf.get('omega_mp','mp_ordinary_loan')
        self._sms_code = cf.get('omega_mp','sms_code')
        