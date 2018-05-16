import requests
from robot.api import logger

from JiaseLibrary.version import VERSION
from JiaseLibrary.keywords.kappa.mp.sys import _SysKeywords
from JiaseLibrary.keywords.kappa.mp.platform import _PaltformKeywords

__version__ = VERSION


class KappaMpLibrary(
    _SysKeywords
    , _PaltformKeywords
):
    """
    kappa-mp 相关的关键字

    """

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    ROBOT_SUPPRESS_NAME = False
    ROBOT_EXIT_ON_FAILURE = True

    def __init__(self
                 , host="127.0.0.1"
                 , port="8011"):
        """

        :param host: 指定kappa-backend-mp的地址
        :param port: 指定kappa-backend-mp的端口
        """
        super(KappaMpLibrary, self).__init__()

        self._host = host
        self._port = port
        self.interface_url = "http://%s:%s" % (self._host, self._port)

        self.session = requests.session()
        self.session.headers["Content-Type"] = "application/json"

