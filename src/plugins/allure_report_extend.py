# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114,C0103,R0903
import os
from tkinter import Tk

from setting.globalconfig import GlobalConfig
from src.dbus_utils import DbusUtils


def wf(f, t):
    f.write(t.encode("unicode_escape").decode() + "\n")


class AllureReportExtend:
    """AllureReportExtend"""

    @staticmethod
    def environment_info(session):
        """写入环境变量"""
        try:
            allure_path = session.config.option.allure_report_dir
        except TypeError:
            return
        if not allure_path:
            return
        allure_fspath_path = os.path.join(
            session.config.invocation_dir,
            allure_path,
            "environment.properties"
        )
        with open(allure_fspath_path, "w+", encoding="utf-8") as _f:
            wf(_f, f"网络地址={GlobalConfig.USERNAME}@{GlobalConfig.HOST_IP}")
            wf(_f, f"系统信息={GlobalConfig.PRODUCT_INFO}")
            wf(_f, f"镜像版本={GlobalConfig.VERSION}")

            screen = Tk()
            wf(_f, f"分辨率={screen.winfo_screenwidth()}x{screen.winfo_screenheight()}")

            try:
                language_code = DbusUtils(
                    "com.deepin.daemon.LangSelector",
                    "/com/deepin/daemon/LangSelector",
                    "com.deepin.daemon.LangSelector",
                ).get_session_properties_value("CurrentLocale")
                wf(_f, f"系统语言={GlobalConfig.LANGUAGE_INI.get(language_code, default=language_code)}")
            except Exception:
                pass

            _display = GlobalConfig.DisplayServer.wayland if GlobalConfig.IS_WAYLAND else GlobalConfig.DisplayServer.x11
            wf(_f, f"显示协议={_display.title()}")

            os_info = os.popen("uname -a").read()
            wf(_f, f"内核信息={os_info}")

            cpu_info = os.popen("cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c").read().replace(" ", "")
            if not cpu_info:
                cpu_info = os.popen("cat /proc/cpuinfo | grep Hardware").read()
            wf(_f, f"CPU信息={cpu_info}")

            mem_info = os.popen("cat /proc/meminfo | grep MemTotal").read()
            wf(_f, f"内存信息={mem_info}")
