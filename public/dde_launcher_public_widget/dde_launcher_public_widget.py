#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
import letmego

from src import sleep, log
from src import Src
from src.custom_exception import ElementNotFound
from public.dde_launcher_public_widget.config import Config

@letmego.mark
@log
# pylint: disable=too-many-ancestors
class DdeLauncherPublicWidget(Src):
    """启动器的方法类"""

    APP_NAME = "dde-launcher"
    DESC = "/usr/bin/dde-launcher"

    def __init__(self):
        kwargs = {}
        kwargs["name"] = self.APP_NAME
        kwargs["description"] = self.DESC
        kwargs["check_start"] = True
        kwargs["config_path"] = Config.UI_INI_PATH
        Src.__init__(self, **kwargs)

    def click_and_input_search_edit_in_launcher_by_attr(self, text):
        """
         在启动器中点击搜索，然后输入
        :param text: 输入的文本
        :return:
        """
        try:
            self.dog.app_element("Form_windowedsearcheredit").click()
        except ElementNotFound:
            self.dog.app_element("Form_searcheredit").click()
        sleep(0.5)
        self.input_message(text)
        sleep(0.5)

    def click_search_edit_on_launcher_by_attr(self):
        """
         移动到启动器上
        :return:
        """
        try:
            self.dog.app_element("Form_windowedsearcheredit").click()
        except ElementNotFound:
            self.dog.app_element("Form_searcheredit").click()

    def click_app_in_lancher_by_attr(self, app_name):
        """
         在启动器中点击应用
        :param app_name: 应用名
        :return:
        """
        self.dog.app_element(f"{app_name}").click()

    def double_click_app_in_lancher_by_attr(self, app_name):
        """
         在启动器中双击应用
        :param app_name: 应用名
        :return:
        """
        self.dog.app_element(f"{app_name}").doubleClick()

    def right_click_app_in_lancher_by_attr(self, app_name):
        """
         在启动器中右键点击应用
        :param app_name: 应用名
        :return:
        """
        self.dog.app_element(f"{app_name}").click(3)

    def select_music_right_menu_in_launcher(self, num):
        """
         在启动器中选择音乐的右键菜单
        :param num: 菜单的第几项
        :return:
        """
        self.click_and_input_search_edit_in_launcher_by_attr("音乐")
        sleep(1)
        self.right_click_app_in_lancher_by_attr("音乐")
        self.select_menu(num)
        sleep(1)

    def click_music_in_launcher_by_attr(self):
        """
         在启动器中点击音乐
        :return:
        """
        self.click_app_in_lancher_by_attr("音乐")

    def click_open_file_manager_in_launcher_by_attr(self):
        """
         在启动器中点击文管
        :return:
        """
        self.click_and_input_search_edit_in_launcher_by_attr("文件管理器")
        self.click_app_in_lancher_by_attr("文件管理器")

    def click_screen_recorder_in_launcher_by_attr(self):
        """
         在启动器中点击截图录屏
        :return:
        """
        self.click_and_input_search_edit_in_launcher_by_attr("截图录屏")
        self.click_app_in_lancher_by_attr("截图录屏")

    def send_file_manager_to_desktop_in_launcher_by_attr(self):
        """
         在launcher中发送到桌面
        :return:
        """
        self.click_and_input_search_edit_in_launcher_by_attr("文件管理器")
        self.right_click_app_in_lancher_by_attr("文件管理器")
        self.select_menu(2)
        sleep(1)

    def open_file_manager_in_launcher_by_right_menu(self):
        """
         在启动器中右键打开应用
        :return:
        """
        self.click_and_input_search_edit_in_launcher_by_attr("文件管理器")
        self.right_click_app_in_lancher_by_attr("文件管理器")
        self.select_menu(1)
        sleep(1)
