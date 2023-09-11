#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
import letmego

from src import Src
from src import log
from public.right_menu_public_widget.right_menu_public_widget import (
    RightMenuPublicWidget,
)
from public.other_public_widget.config import Config

@letmego.mark
@log
# pylint: disable=too-many-ancestors
class DeepinCompressPublicWidget(Src, RightMenuPublicWidget):
    """DeepinCompressPublicWidget"""

    APP_NAME = "deepin-compressor"
    DESC = "/usr/bin/deepin-compressor"

    def __init__(self):
        kwargs = {}
        kwargs["name"] = self.APP_NAME
        kwargs["description"] = self.DESC
        kwargs["check_start"] = True
        kwargs["config_path"] = Config.UI_INI_PATH
        Src.__init__(self, **kwargs)

    def click_compress_btn_in_compress_window_by_ui(self):
        """
         点击压缩按钮
        :return:
        """
        self.click(*self.ui.btn_center("压缩按钮"))

    def click_save_to_btn_in_compress_window_by_ui(self):
        """
         点击保存到按钮
        :return:
        """
        self.click(*self.ui.btn_center("保存到按钮"))

    def click_replace_btn_in_compress_window_by_ui(self):
        """
         压缩同名提示，点击替换按钮
        :return:
        """
        self.click(*self.ui.btn_center("替换按钮"))

    @classmethod
    def close_compress_by_cmd(cls):
        """
         关闭压缩
        :return:
        """
        cls.kill_process("deepin-compressor")
