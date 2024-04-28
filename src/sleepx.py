#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
from time import sleep as slp
from setting.globalconfig import GlobalConfig
from src import logger


def sleep(second: [float, int]):
    """
     重写sleep方法
     1、增加等待时间的日志
     2、根据不同CPU架构进行放大
    :param second: 等待时间
    :return:
    """
    sys_arch = GlobalConfig.SYS_ARCH
    multiple = float(GlobalConfig.slp_cfg.get(sys_arch))
    mult_sec = second * multiple
    logger.debug(f"sleep {second} s [{sys_arch} * {multiple} = {mult_sec}]")
    slp(mult_sec)
