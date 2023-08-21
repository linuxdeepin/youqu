#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
from setting.globalconfig import GlobalConfig


def skipif_platform(args: str):
    """平台跳过
    skipif_platform-aarch64
    """
    _skip_key = args.split("&")
    for key in _skip_key:
        if GlobalConfig.SYS_ARCH == key:
            return True
    return False


def skipif_xdg_type(args: str):
    """skipif wayland or x11
    skipif_xdg_type-wayland
    """
    _skip_key = args.split("&")
    for key in _skip_key:
        if GlobalConfig.DISPLAY_SERVER == key:
            return True
    return False


def skipif_cpu_name(args: str):
    """skipif cpu name
    使用 sudo dmidecode -s system-product-name 查看机器的cpu型号
    剔除中横线和&符号，比如：KLVV-W5821，标签记录为 KLVVW5821
    """
    import os
    _skip_key = args.split("&")
    for key in _skip_key:
        if os.popen(
                f"echo '{GlobalConfig.PASSWORD}'| "
                "sudo -S dmidecode -s system-product-name | awk '{print $NF}'"
        ).read().strip("\n").replace("-", "").replace("&", "") == key:
            return True
    return False
