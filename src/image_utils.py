#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
# pylint: disable=E0401,C0413,R0903,W0707,W0611
try:
    import cv2 as cv

    GET_OPENCV_FORM_RPC = False
except ModuleNotFoundError:
    GET_OPENCV_FORM_RPC = True

from image_center import ImageCenter
from image_center.conf import setting as image_setting

from setting import conf

image_setting.PORT = conf.OPENCV_PORT
image_setting.SERVER_IP = conf.OPENCV_SERVER_HOST
image_setting.NETWORK_RETRY = int(conf.OPENCV_NETWORK_RETRY)
image_setting.PAUSE = float(conf.OPENCV_PAUSE)
image_setting.TIMEOUT = float(conf.OPENCV_TIMEOUT)
image_setting.MAX_MATCH_NUMBER = int(conf.OPENCV_MAX_MATCH_NUMBER)


class ImageUtils(ImageCenter):
    """图像识别的工具类"""
