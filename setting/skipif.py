#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only

"""
此配置文件用于标签化管理方案实现条件判断的配置项；
在CSV文件中“跳过原因”列填入函数名和参数，即可实现条件判断；
比如：
在CSV文件中“跳过原因”列填入：skipif_platform-aarch64
    函数名称为：skipif_platform，比如是此文件中定义了的函数；
    参数为：aarch64，多个参数用 & 符号连接；
    函数名与参数之间用 - （中横线）连接；
"""
import os

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
    _skip_key = args.split("&")
    for key in _skip_key:
        if os.popen(
                f"echo '{GlobalConfig.PASSWORD}'| "
                "sudo -S dmidecode -s system-product-name | awk '{print $NF}'"
        ).read().strip("\n").replace("-", "").replace("&", "") == key:
            return True
    return False


def skipif_os_version(args: str):
    """
    系统版本跳过
    :param args: 1060&1070
    :return:
    """
    _skip_key = args.split("&")
    for key in _skip_key:
        if key == GlobalConfig.OS_VERSION.get("MinorVersion"):
            return True
    return False
