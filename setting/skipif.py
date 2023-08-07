#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
from setting.globalconfig import GlobalConfig


def skipif_platform(args: str):
    """平台跳过"""
    _skip_key = args.split("&")
    for key in _skip_key:
        if GlobalConfig.SYS_ARCH == key:
            return True
    return False
