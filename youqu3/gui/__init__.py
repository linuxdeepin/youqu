from youqu3 import setting
from youqu3.exceptions import YouQuPluginDependencyError

try:

    from pylinuxauto.config import config as pylinuxauto_config

    pylinuxauto_config.OCR_SERVER_IP = setting.OCR_SERVER_IP
    pylinuxauto_config.IMAGE_SERVER_IP = setting.IMAGE_SERVER_IP

    import pylinuxauto as pylinuxauto
    from youqu3.gui.rpc_gui import RpcGui

except ImportError:
    raise YouQuPluginDependencyError("pylinuxauto")
