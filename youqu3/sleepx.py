#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only

from time import sleep as slp
from youqu3 import logger
from youqu3 import setting


def sleep(second: [float, int]):
    """
    重写sleep方法
    1.增加等待时间的日志
    2.根据不同CPU架构进行放大
    :param second: 等待时间
    :return:
    """
    multiple = getattr(setting.Sleepx, setting.SYS_ARCH)
    mult_sec = second * multiple
    logger.debug(f"sleep {second} s [{setting.SYS_ARCH} * {multiple} = {mult_sec}]")
    slp(mult_sec)

if __name__ == '__main__':
    sleep(1)
