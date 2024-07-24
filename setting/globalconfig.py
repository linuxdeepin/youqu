#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import pathlib
from configparser import RawConfigParser
from enum import Enum
from enum import unique
from getpass import getuser
from os import popen
from os.path import abspath
from os.path import dirname
from os.path import exists
from os.path import join
from platform import machine
from time import strftime


class GetCfg:
    """Gets the value in the configuration file"""

    def __init__(self, config_file: str, option: [str, None] = None):
        self.config_file = config_file
        self.option = option
        self.conf = RawConfigParser()
        self.conf.read(self.config_file, encoding="utf-8")

    def get(self, key: str, op: [str, None] = None, default=None) -> str:
        if op is None and self.option is not None:
            op = self.option
        if op is None and self.option is None:
            raise ValueError("option is None")
        return self.conf.get(op, key, fallback=default)

    def get_bool(self, key: str, op: [str, None] = None, default=False) -> bool:
        if op is None and self.option is not None:
            op = self.option
        if op is None and self.option is None:
            raise ValueError("option is None")
        return self.conf.getboolean(op, key, fallback=default)


class _GlobalConfig:
    """Basic framework global configuration"""

    PROJECT_NAME = "YouQu"

    class DirName:
        SRC = "src"
        APPS = "apps"
        DOCS = "docs"
        PUBLIC = "public"
        REPORT = "report"
        SETTING = "setting"

    # ====================== ABSOLUTE PATH ======================
    # Root dir
    ROOT_DIR = dirname(dirname(abspath(__file__)))
    # apps path
    APPS_PATH = join(ROOT_DIR, DirName.APPS)
    # setting path
    SETTING_PATH = join(ROOT_DIR, DirName.SETTING)
    # Default does not exist
    REPORT_PATH = join(ROOT_DIR, DirName.REPORT)

    # username
    USERNAME = getuser()
    HOME = str(pathlib.Path.home())

    # ====================== GLOBAL CONFIG INI ======================
    # Get config file object
    GLOBAL_CONFIG_FILE_PATH = join(SETTING_PATH, "globalconfig.ini")
    # [run]
    run_cfg = GetCfg(GLOBAL_CONFIG_FILE_PATH, "run")
    APP_NAME = run_cfg.get("APP_NAME", default="")
    KEYWORDS = run_cfg.get("KEYWORDS", default="")
    TAGS = run_cfg.get("TAGS", default="")
    CASE_FILE = run_cfg.get("CASE_FILE", default="")
    RERUN = run_cfg.get("RERUN", default=1)
    RECORD_FAILED_CASE = run_cfg.get("RECORD_FAILED_CASE", default=1)
    MAX_FAIL = run_cfg.get("MAX_FAIL", default=1)
    CASE_TIME_OUT = run_cfg.get("CASE_TIME_OUT", default=200)
    CLEAN_ALL = run_cfg.get("CLEAN_ALL", default="yes")
    RESOLUTION = run_cfg.get("RESOLUTION", default="1920x1080")
    NOSKIP = run_cfg.get_bool("NOSKIP", default=False)
    IFIXED = run_cfg.get_bool("IFIXED", default=False)
    DURING_FAIL = run_cfg.get_bool("DURING_FAIL", default=False)
    AUTOSTART = run_cfg.get_bool("AUTOSTART", default=False)
    TOP = run_cfg.get("TOP", default="")
    REPEAT = run_cfg.get("REPEAT", default="")
    DEB_PATH = run_cfg.get("DEB_PATH", default="~/Downloads/")
    DEBUG = run_cfg.get_bool("DEBUG", default=False)
    PASSWORD = run_cfg.get("PASSWORD", default="1")
    if not PASSWORD:
        raise ValueError("测试机密码不能未空")
    IMAGE_MATCH_NUMBER = run_cfg.get("IMAGE_MATCH_NUMBER", default=1)
    IMAGE_MATCH_WAIT_TIME = run_cfg.get("IMAGE_MATCH_WAIT_TIME", default=1)
    IMAGE_RATE = run_cfg.get("IMAGE_RATE", default=0.8)
    SCREEN_CACHE = run_cfg.get("SCREEN_CACHE", default="/tmp/screen.png")
    TMPDIR = run_cfg.get("TMPDIR", default="/tmp/tmpdir")
    SYS_THEME = run_cfg.get("SYS_THEME", default="deepin")

    OCR_SERVER_HOST = run_cfg.get("OCR_SERVER_HOST", default="localhost")
    OCR_PORT = run_cfg.get("OCR_PORT", default="8890")
    OCR_NETWORK_RETRY = run_cfg.get("OCR_NETWORK_RETRY", default=1)
    OCR_PAUSE = run_cfg.get("OCR_PAUSE", default=1)
    OCR_TIMEOUT = run_cfg.get("OCR_TIMEOUT", default=5)
    OCR_MAX_MATCH_NUMBER = run_cfg.get("OCR_MAX_MATCH_NUMBER", default=100)

    OPENCV_SERVER_HOST = run_cfg.get("OPENCV_SERVER_HOST", default="localhost")
    OPENCV_PORT = run_cfg.get("OPENCV_PORT", default="8889")
    OPENCV_NETWORK_RETRY = run_cfg.get("OPENCV_NETWORK_RETRY", default=1)
    OPENCV_PAUSE = run_cfg.get("OPENCV_PAUSE", default=1)
    OPENCV_TIMEOUT = run_cfg.get("OPENCV_TIMEOUT", default=5)
    OPENCV_MAX_MATCH_NUMBER = run_cfg.get("OPENCV_MAX_MATCH_NUMBER", default=100)

    SLAVES = run_cfg.get("SLAVES", default="")
    USER_DATE_DIR = run_cfg.get("USER_DATE_DIR", default="").replace("{{HOME}}", HOME)
    EXECUTABLE_PATH = run_cfg.get("EXECUTABLE_PATH", default="")

    # [remote]
    remote_cfg = GetCfg(GLOBAL_CONFIG_FILE_PATH, "remote")
    SEND_CODE = remote_cfg.get_bool("SEND_CODE", default=True)
    BUILD_ENV = remote_cfg.get_bool("BUILD_ENV", default=False)
    CLIENT_PASSWORD = remote_cfg.get("CLIENT_PASSWORD", default="1")
    PARALLEL = remote_cfg.get_bool("PARALLEL", default=True)
    CLEAN_SERVER_REPORT_DIR = remote_cfg.get_bool("CLEAN_SERVER_REPORT_DIR", default=False)
    CLEAN_CLIENT_REPORT_DIR = remote_cfg.get_bool("CLEAN_CLIENT_REPORT_DIR", default=True)
    SCAN = remote_cfg.get("SCAN", default="300")
    CLIENTS = remote_cfg.get("CLIENTS", default="")

    # [report]
    report_cfg = GetCfg(GLOBAL_CONFIG_FILE_PATH, "report")
    REPORT_TITLE = report_cfg.get("REPORT_TITLE", default="YouQu Report")
    REPORT_NAME = report_cfg.get("REPORT_NAME", default="YouQu Report")
    REPORT_LANGUAGE = report_cfg.get("REPORT_LANGUAGE", default="zh")
    REPORT_FORMAT = report_cfg.get("REPORT_FORMAT", default="allure, xml, json")
    ALLURE_REPORT_PATH = join(
        ROOT_DIR, report_cfg.get("ALLURE_REPORT_PATH", default="report/")
    )
    XML_REPORT_PATH = join(
        ROOT_DIR, report_cfg.get("XML_REPORT_PATH", default="report/")
    )
    JSON_REPORT_PATH = join(
        ROOT_DIR, report_cfg.get("JSON_REPORT_PATH", default="report/")
    )

    # [pmsctl]
    pms_cfg = GetCfg(GLOBAL_CONFIG_FILE_PATH, "pmsctl")
    PMS_USER = pms_cfg.get("PMS_USER", default="")
    PMS_PASSWORD = pms_cfg.get("PMS_PASSWORD", default="")
    SUITE_ID = pms_cfg.get("SUITE_ID", default="")
    SEND_PMS = pms_cfg.get("SEND_PMS", default="")
    if SEND_PMS not in ("", "async", "finish"):
        raise ValueError
    TASK_ID = pms_cfg.get("TASK_ID", default="")
    TRIGGER = pms_cfg.get("TRIGGER", default="auto")
    if TRIGGER not in ("auto", "hand"):
        raise ValueError
    SEND_PMS_RETRY_NUMBER = pms_cfg.get("SEND_PMS_RETRY_NUMBER", default=2)
    CASE_FROM = pms_cfg.get("CASE_FROM", default="caselib")
    CSV_NAME_TO_PMS = pms_cfg.get("CSV_NAME_TO_PMS", default="")

    # [csvctl]
    csv_cfg = GetCfg(GLOBAL_CONFIG_FILE_PATH, "csvctl")
    PY_ID_TO_CSV = csv_cfg.get_bool("PY_ID_TO_CSV", default=False)
    EXPORT_CSV_FILE = csv_cfg.get("EXPORT_CSV_FILE", default="")
    EXPORT_CSV_HEARD = csv_cfg.get(
        "EXPORT_CSV_HEARD", default="用例级别,用例类型,测试级别,是否跳过"
    ).replace(" ", "")

    # [log_cli]
    log_cli = GetCfg(GLOBAL_CONFIG_FILE_PATH, "log_cli")
    LOG_LEVEL = log_cli.get("LOG_LEVEL", default="INFO")
    CLASS_NAME_STARTSWITH = tuple(
        log_cli.get("CLASS_NAME_STARTSWITH", default="Assert")
        .replace(" ", "")
        .split(",")
    )
    CLASS_NAME_ENDSWITH = tuple(
        log_cli.get("CLASS_NAME_ENDSWITH", default="Widget").replace(" ", "").split(",")
    )
    CLASS_NAME_CONTAIN = tuple(
        log_cli.get("CLASS_NAME_CONTAIN", default="ShortCut")
        .replace(" ", "")
        .split(",")
    )

    # [git]
    git_cfg = GetCfg(GLOBAL_CONFIG_FILE_PATH, "git")
    GIT_URL = git_cfg.get("GIT_URL", default="")
    GIT_USER = git_cfg.get("GTI_USER", default="")
    GIT_PASSWORD = git_cfg.get("GIT_PASSWORD", default="")
    BRANCH = git_cfg.get("BRANCH", default="")
    DEPTH = git_cfg.get("DEPTH", default="")
    START_DATE = git_cfg.get("START_DATE", default="")
    END_DATE = git_cfg.get("END_DATE", default="")

    # ====================== 动态获取变量 ======================
    VERSION = ""
    if exists("/etc/os-version"):
        version_cfg = GetCfg("/etc/os-version", "Version")
        VERSION = (version_cfg.get("EditionName[zh_CN]") or "") + (
                version_cfg.get("MinorVersion") or ""
        )
    # IP
    HOST_IP = str(popen("hostname -I |awk '{print $1}'").read()).strip("\n").strip()
    PRODUCT_INFO = ""
    if exists("cat /etc/product-info"):
        PRODUCT_INFO = popen("cat /etc/product-info").read()
    # machine type
    # e.g. x86_64
    SYS_ARCH = machine()
    LANGUAGE_INI = GetCfg(join(SETTING_PATH, "template/language.ini"), "language")

    current_tag = GetCfg(f"{ROOT_DIR}/CURRENT", "current").get("tag")

    class ArchName:
        x86 = "x86_64"
        arm = "aarch64"
        mips = "mips64"
        longxin = "loongarch64"
        sw = "sw_64"

    class ReportFormat:
        ALLURE = "allure"
        XML = "xml"
        JSON = "json"

    TIME_STRING = strftime("%Y%m%d%H%M%S")

    slp_cfg = GetCfg(f"{SETTING_PATH}/sleepx.ini", "sleepx")

    # 显示服务器
    # 直接读环境变量XDG_SESSION_TYPE会有问题，采用读文件的方式获取
    DISPLAY_SERVER = (
                         popen("cat ~/.xsession-errors | grep XDG_SESSION_TYPE | head -n 1")
                         .read()
                         .split("=")[-1]
                         .strip("\n")
                     ) or ("x11" if popen("ps -ef | grep -v grep | grep kwin_x11").read() else "wayland")

    class DisplayServer:
        wayland = "wayland"
        x11 = "x11"

    if DISPLAY_SERVER not in (DisplayServer.x11, DisplayServer.wayland):
        raise EnvironmentError(f"DISPLAY_SERVER: {DISPLAY_SERVER} why?")

    IS_X11 = DISPLAY_SERVER == DisplayServer.x11
    IS_WAYLAND = DISPLAY_SERVER == DisplayServer.wayland

    top_cmd = "top -b -d 3 -w 512"

    GITHUB_URL = "https://github.com/linuxdeepin/youqu"
    DOCS_URL = "https://youqu.uniontech.com/"
    PyPI_URL = "https://pypi.org/project/youqu"

    LETMEGO_DEBUG = True
    DTK_DISPLAY = False


GlobalConfig = _GlobalConfig()


@unique
class ConfStr(Enum):
    SKIP = "skip"
    SKIPIF = "skipif"
    FIXED = "fixed"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    REMOVED = "removed"
    RERUN = "rerun"
    AUTO = "auto"
    ASYNC = "async"
    FINISH = "finish"
    SKIP_INDEX = "skip_index"
    FIXED_INDEX = "fixed_index"
    REMOVED_INDEX = "removed_index"
    PMS_ID_INDEX = "pms_id_index"


@unique
class FixedCsvTitle(Enum):
    case_id = "脚本ID"
    pms_case_id = "*PMS用例ID"
    case_level = "用例级别"
    case_type = "用例类型"
    device_type = "*设备类型"
    case_from = "一二级bug自动化"
    online_obj = "*上线对象"
    skip_reason = "跳过原因"
    fixed = "确认修复"
    removed = "废弃用例"


@unique
class SystemPath(Enum):
    SRC_PATH = join(GlobalConfig.ROOT_DIR, "src")
    DEPENDS_PATH = join(GlobalConfig.ROOT_DIR, "src/depends")
    APPS_PATH = GlobalConfig.APPS_PATH
