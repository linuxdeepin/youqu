#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
import letmego

from src import logger, log
from src import Src
from public.open_mode_public_widget.config import Config

@letmego.mark
@log
# pylint: disable=too-many-ancestors
class OpenModePublicWidget(Src):
    """
    文件打开方式封装
    """

    @classmethod
    def click_open_mode_image(cls, pic):
        """
         点击右键菜单中的相应选项
        :param pic: 图片路径
        :return
        """
        cls.click(*cls.find_image(f"{Config.PIC_RES_PATH}/" + pic))

    @classmethod
    def click_txt_editor_in_open_mode_window_by_image(cls):
        """
         点击打开方式窗口中的“文本编辑器”
        :return:
        """
        cls.click_open_mode_image("text_editor")
        logger.info("点击打开方式窗口中的“文本编辑器")

    @classmethod
    def click_file_manager_in_open_mode_window_by_image(cls):
        """
         点击打开方式窗口中的“文件管理器”
        :return:
        """
        cls.click_open_mode_image("file_manager")
        logger.info("点击打开方式窗口中的“文件管理器”")

    @classmethod
    def click_determine_in_open_mode_window_by_image(cls):
        """
         点击打开方式窗口中的“确定”
        :return:
        """
        cls.click_open_mode_image("determine")
        logger.info("点击确认")
