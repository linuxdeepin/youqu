#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
from funnylog import logger

from setting import conf
from src import Src
from src.cmdctl import CmdCtl
from src.dogtail_utils import DogtailUtils
from src.remotectl._remote_dogtail_ctl import remote_dogtail_ctl as remote_dogtail_ctl
from src.remotectl._remote_other_ctl import remote_other_ctl as remote_other_ctl
from src.shortcut import ShortCut


class Remote(ShortCut, CmdCtl):
    def __init__(self, ip, user, password, transfer_appname=None, restart_service=False):
        self.user = user
        self.ip = ip
        self.password = password
        self.transfer_appname = transfer_appname
        self.restart_service = restart_service
        self.tmp_obj = None

    def __getattribute__(self, item):
        if not item.startswith("__") and not item.endswith("__"):
            for cls_obj in [ShortCut, CmdCtl]:
                if hasattr(cls_obj, item):
                    self.tmp_obj = {"cls_obj": cls_obj, "item_obj": getattr(cls_obj, item)}
                    while True:
                        if hasattr(cls_obj, item):
                            delattr(cls_obj, item)
                        else:
                            break
        return super().__getattribute__(item)

    def __getattr__(self, item):
        def func(*args, **kwargs):
            ar = ""
            if args:
                for arg in args:
                    ar += f"'{arg}', "
            if kwargs:
                for k, v in kwargs.items():
                    ar += f"{k}='{v}', "
            logger.info(
                f"Remote(user='{self.user}', ip='{self.ip}', password='{self.password}').rctl.{item}({ar.rstrip(', ')})"
            )
            value = None
            try:
                value = getattr(self.rctl, item)(*args, **kwargs)
            finally:
                if self.tmp_obj:
                    setattr(self.tmp_obj["cls_obj"], item, self.tmp_obj["item_obj"])
                    self.tmp_obj = None
            return value

        return func

    @property
    def rdog(self) -> DogtailUtils:
        return remote_dogtail_ctl(
            user=self.user,
            ip=self.ip,
            password=self.password,
            restart_service=self.restart_service,
        )

    def click_element_by_attr(self, element, button=1):
        self.rdog.element_click(element, button=button)

    @property
    def rctl(self) -> Src:
        return remote_other_ctl(
            user=self.user,
            ip=self.ip,
            password=self.password,
            restart_service=self.restart_service,
        )

    @property
    def rctl_plus(self) -> Src:
        return remote_other_ctl(
            user=self.user,
            ip=self.ip,
            password=self.password,
            transfer_appname=self.transfer_appname,
            restart_service=self.restart_service,
        )

    def find_image(self, image_path):
        _image_path = image_path.replace(conf.HOME, "~", 1)
        return self.rctl_plus.find_image(_image_path)


if __name__ == '__main__':
    a = Remote(
        user="uos",
        ip="10.8.7.55",
        password="1",
    ).rcmd.sudo_run_cmd("systemctl restart lightdm.service")
    # ).run_cmd("ls")
    print(a)
