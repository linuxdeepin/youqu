#!/usr/bin/env python3 # pylint: disable=too-many-lines
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
import os
import re
from configparser import ConfigParser
from configparser import NoOptionError

from src import logger


def get_desktop_file_location_by_config(name):
    """
     根据桌面配置文件获取文件或者文件夹坐标
    :param name: 文件名称
    :return: 坐标
    """
    # 不同图标大小的高宽 y，x
    num = [(102, 62), (118, 92), (148, 120), (172, 174), (207, 242)]
    desktop_conf_file = os.path.expanduser("~/.config/deepin/dde-desktop/dde-desktop.conf")
    conf = ConfigParser()
    if not os.path.exists(desktop_conf_file):
        os.system("cd ~/Desktop;touch .test_desktop;sleep 1;rm -rf .test_desktop")
    try:
        conf.read(os.path.expanduser(desktop_conf_file))
        level = int(conf.get("GeneralConfig", "IconLevel", fallback=1))
    except NoOptionError as exc:
        raise EnvironmentError(f"{desktop_conf_file} 可能不存在") from exc
    for _x, _y in dict(conf["SingleScreen"]).items():
        frame = re.sub(
            r"\\x[0-9a-fA-F]{2,4}",
            lambda i: chr(int(i.group().replace(r"\x", ""), 16)),
            _y,
        )
        if frame.endswith(name):
            axes = _x.split("_")[::-1]
            _y, _x = map(
                lambda i: int(i[0]) * int(i[1]) + int(i[1]) / 2,
                zip(axes, num[level]),
            )
            logger.info(f"{name}坐标为{str(_x)},{str(_x)}")
            return int(_x), int(_y)
    raise ValueError(f"{name} 未找到")
