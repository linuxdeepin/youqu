import dataclasses
import enum
import os

from youqu3._setting._dynamic import _DynamicSetting


class _Setting(_DynamicSetting):
    """YouQu Config"""

    PASSWORD: str = os.environ.get("YOUQU_PASSWORD") or "1"

    TIMEOUT = os.environ.get("YOUQU_TIMEOUT") or 300
    LOG_LEVEL = os.environ.get("YOUQU_LOG_LEVEL") or "INFO"
    RERUNS = os.environ.get("YOUQU_RERUNS") or 1
    RECORD_FAILED_NUM = os.environ.get("YOUQU_RECORD_FAILED_NUM") or 1

    # OCR
    OCR_NETWORK_RETRY = 1
    OCR_PAUSE = 1
    OCR_TIMEOUT = 5
    OCR_MAX_MATCH_NUMBER = 100
    OCR_PORT = 8890
    OCR_SERVER_IP = "10.8.13.7/10.8.13.66/10.8.13.55/10.8.13.100"

    # IMAGE
    IMAGE_NETWORK_RETRY = 1
    IMAGE_PAUSE = 1
    IMAGE_TIMEOUT = 5
    IMAGE_MAX_MATCH_NUMBER = 100
    IMAGE_PORT = 8889
    IMAGE_SERVER_IP = "10.8.12.175/10.8.12.130/10.8.12.181/10.8.12.216"

    # REPORT SERVER
    REPORT_SERVER_IP = "10.8.12.47/10.8.12.37"
    REPORT_PORT = 5656
    REPORT_SERVER_SSH_USER = "uos"
    REPORT_SERVER_SSH_PASSWORD = "1"
    REPORT_BASE_PATH = "~/report"

    # REMOTE

    # SLAVES
    SLAVES = os.environ.get("SLAVES")

    # WEBUI
    EXECUTABLE_PATH = f"{_DynamicSetting.HOME}/.config/browser"
    USER_DATE_DIR = "/usr/bin/browser"
    HEADLESS = True if os.environ.get("HEADLESS") is None else False

    PYPI_MIRROR = "https://pypi.tuna.tsinghua.edu.cn/simple"

    @dataclasses.dataclass
    class Sleepx:
        x86_64: [float, int] = 1
        aarch64: [float, int] = 1.5
        loongarch64: [float, int] = 2
        mips64: [float, int] = 2.5
        sw64: [float, int] = 2.5

    @enum.unique
    class FixedCsvTitle(enum.Enum):
        case_id = "脚本ID"
        skip_reason = "跳过原因"
        fixed = "确认修复"
        removed = "废弃用例"


setting = _Setting()
