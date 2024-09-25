#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
from typing import Union, List

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
        self.rdog.element_click(element, button)

    def get_element_children_txt(self, element):
        return self.rdog.get_element_children_text(element)

    def get_element_center(self, element):
        return self.rdog.element_center(element)

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

    def find_image(
            self,
            *image,
            rate: Union[float, int] = None,
            multiple: bool = False,
            picture_abspath: str = None,
            screen_bbox: List[int] = None,
            log_level: str = "info",
            network_retry: int = None,
            pause: [int, float] = None,
            timeout: [int, float] = None,
            max_match_number: int = None
    ):
        """
         在屏幕中区寻找小图，返回坐标，
         如果找不到，根据配置重试次数，每次间隔1秒
        :param picture_abspath: 原始图片绝对路径，不指定时截全屏
        :param image: 模板图片路径
        :param rate: 相似度
        :param multiple: 是否返回匹配到的多个目标
        :param screen_bbox: 截取屏幕上指定区域图片（仅支持X11下使用）；
            [x, y, w, h]
            x: 左上角横坐标；y: 左上角纵坐标；w: 宽度；h: 高度；根据匹配度返回坐标
        :param log_level: 日志级别
        :param network_retry: 连接服务器重试次数
        :param pause: 图像识别重试的间隔时间
        :param timeout: 最大匹配超时,单位秒
        :param max_match_number: 最大匹配次数
        :return: 坐标元组
        """
        _image_path = tuple([_path.replace(conf.HOME, "~", 1) for _path in image])
        if picture_abspath:
            picture_abspath = picture_abspath.replace(conf.HOME, "~", 1)
        return self.rctl_plus.find_image_remote(
            _image_path, rate, multiple, picture_abspath, screen_bbox, log_level,
            network_retry, pause, timeout, max_match_number
        )

    def ocr(
            self,
            *target,
            picture_abspath: str = None,
            similarity: [int, float] = 0.6,
            return_default: bool = False,
            return_first: bool = False,
            lang: str = "ch",
            network_retry: int = None,
            pause: [int, float] = None,
            timeout: [int, float] = None,
            max_match_number: int = None
    ):
        """
        通过 OCR 进行识别。
        :param target:
            目标字符,识别一个字符串或多个字符串,并返回其在图片中的坐标;
            如果不传参，返回图片中识别到的所有字符串。
        :param picture_abspath: 要识别的图片路径，如果不传默认截取全屏识别。
        :param similarity: 匹配度。
        :param return_default: 返回识别的原生数据。
        :param return_first: 只返回第一个,默认为 False,返回识别到的所有数据。
        :param lang: `ch`, `en`, `fr`, `german`, `korean`, `japan`
        :param network_retry: 连接服务器重试次数
        :param pause: 重试间隔时间,单位秒
        :param timeout: 最大匹配超时,单位秒
        :param max_match_number: 最大匹配次数
        :return: 返回的坐标是目标字符串所在行的中心坐标。
        """
        if picture_abspath:
            picture_abspath = picture_abspath.replace(conf.HOME, "~", 1)
        return self.rctl_plus.ocr_remote(target, picture_abspath, similarity, return_default, return_first, lang,
                                         network_retry,
                                         pause, timeout, max_match_number)

if __name__ == '__main__':
    a = Remote(
        user="uos",
        ip="10.8.7.55",
        password="1",
    ).rcmd.sudo_run_cmd("systemctl restart lightdm.service")
    # ).run_cmd("ls")
    print(a)
