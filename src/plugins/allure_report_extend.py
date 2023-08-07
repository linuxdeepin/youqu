# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114,C0103,R0903
import os
from tkinter import Tk

from setting.globalconfig import GlobalConfig
from src.dbus_utils import DbusUtils


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
        allure_fspath_path = os.path.join(session.config.invocation_dir, allure_path)
        with open(
                allure_fspath_path + "/environment.properties", "w+", encoding="utf-8"
        ) as _f:
            _f.write(
                f"网络地址={GlobalConfig.HOST_IP}".encode("unicode_escape").decode() + "\n"
            )
            _f.write(
                f"系统信息={GlobalConfig.PRODUCT_INFO}".encode("unicode_escape").decode()
                + "\n"
            )
            _f.write(
                f"镜像版本={GlobalConfig.VERSION}".encode("unicode_escape").decode() + "\n"
            )
            screen = Tk()
            x = screen.winfo_screenwidth()
            y = screen.winfo_screenheight()
            _f.write(f"分辨率={x}x{y}".encode("unicode_escape").decode() + "\n")
            language_code = DbusUtils(
                "com.deepin.daemon.LangSelector",
                "/com/deepin/daemon/LangSelector",
                "com.deepin.daemon.LangSelector",
            ).get_session_properties_value("CurrentLocale")
            _f.write(
                # pylint: disable=line-too-long
                f"系统语言={GlobalConfig.LANGUAGE_INI.get(language_code, default=language_code)}".encode(
                    "unicode_escape"
                ).decode()
            )
