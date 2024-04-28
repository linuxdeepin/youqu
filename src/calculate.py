#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
import math
from xmlrpc.client import ServerProxy

from setting.globalconfig import GlobalConfig

try:
    import numpy as np

    GET_NP_FROM_RPC = False
except ModuleNotFoundError:
    GET_NP_FROM_RPC = True

from src import logger


class Calculate:
    """Calculate"""

    @staticmethod
    def coordinate_distance(start: tuple, end: tuple):
        """
         计算两个坐标之间的直线距离
        :param start: 起始坐标
        :param end: 终止坐标
        :return: 两点之间距离
        """
        if GET_NP_FROM_RPC:
            server = ServerProxy(GlobalConfig.OPENCV_SERVER_HOST, allow_none=True)
            return server.coordinate_distance(start, end)
        position_start = np.array(start)
        position_end = np.array(end)
        position = position_end - position_start
        return math.hypot(position[0], position[1])

    @staticmethod
    def translational_coordinates(start: tuple, relative: tuple):
        """
         计算坐标平移
        :param start: 起始坐标
        :param relative: 平移的相对坐标
        :return: 平移后的坐标
        """
        if GET_NP_FROM_RPC:
            server = ServerProxy(GlobalConfig.OPENCV_SERVER_HOST, allow_none=True)
            return server.translational_coordinates(start, relative)
        position_start = np.array(start)
        position_end = np.array(relative)
        _c = np.sum([position_start, position_end], axis=0)
        logger.debug(f"平移坐标 “{_c}”")
        return _c
