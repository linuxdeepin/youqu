#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
import letmego

from src import Src, log
from public.right_menu_public_widget.right_menu_public_widget import (
    RightMenuPublicWidget,
)
from public.other_public_widget.config import Config

@letmego.mark
@log
# pylint: disable=too-many-ancestors
class DeepinManualPublicWidget(Src, RightMenuPublicWidget):
    """DeepinManualPublicWidget"""
    APP_NAME = "deepin-manual"
    DESC = "/usr/bin/dman"

    def __init__(self):
        kwargs = {}
        kwargs["name"] = self.APP_NAME
        kwargs["description"] = self.DESC
        kwargs["check_start"] = True
        kwargs["config_path"] = Config.UI_INI_PATH
        Src.__init__(self, **kwargs)

    @classmethod
    def find_help_element_image(cls, *elements):
        """
         通过图片查找帮助元素坐标
        :param elements:
        :return:
        """
        element = tuple(
            map(lambda x: f"{Config.PIC_RES_PATH}/help/elements/{x}", elements)
        )
        return cls.find_image(*element)

    def click_close_btn_in_help_title_by_attr(self):
        """
         标题栏上点击“X“关闭帮助窗口
        :return:
        """
        self.dog.find_element_by_attr(
            "$/DMainWindow/DMainWindowTitlebar/DTitlebarRightArea/"
            "DTitlebarButtonArea//DTitlebarDWindowCloseButton"
        ).click()


if __name__ == "__main__":
    DeepinManualPublicWidget().click_close_btn_in_help_title_by_attr()
