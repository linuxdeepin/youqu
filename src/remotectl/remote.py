#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
from src.remotectl._remote_dogtail_ctl import remote_dogtail_ctl as remote_dogtail_ctl
from src.remotectl._remote_other_ctl import remote_other_ctl as remote_other_ctl
from src.dogtail_utils import DogtailUtils
from src import Src
from setting import conf


class Remote:
    def __init__(self, ip, user, password, transfer_appname=None):
        self.user = user
        self.ip = ip
        self.password = password
        self.transfer_appname = transfer_appname

    @property
    def rdog(self) -> DogtailUtils:
        return remote_dogtail_ctl(user=self.user, ip=self.ip, password=self.password)

    def click_element_by_attr(self, element, button=1):
        self.rdog.element_click(element, button=button)

    @property
    def rctl(self) -> Src:
        return remote_other_ctl(user=self.user, ip=self.ip, password=self.password)

    def click(self, x=None, y=None):
        self.rctl.click(_x=x, _y=y)

    def right_click(self, x=None, y=None):
        self.rctl.right_click(_x=x, _y=y)

    def double_click(self, x=None, y=None):
        self.rctl.double_click(_x=x, _y=y)

    def hot_key(self, *args):
        self.rctl.hot_key(*args)

    @property
    def rctl_plus(self) -> Src:
        return remote_other_ctl(
            user=self.user, ip=self.ip, password=self.password, transfer_appname=self.transfer_appname
        )

    def find_image(self, image_path):
        _image_path = image_path.replace(conf.HOME, "~", Maximum=1)
        return self.rctl_plus.find_image(_image_path)
