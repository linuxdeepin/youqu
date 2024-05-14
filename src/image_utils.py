#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
from typing import Union, List

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
image_setting.IMAGE_RATE = float(conf.IMAGE_RATE)


class ImageUtils(ImageCenter):
    """图像识别的工具类"""

    @classmethod
    def find_image_remote(
            cls,
            widget: tuple,
            rate: Union[float, int] = None,
            multiple: bool = False,
            picture_abspath: str = None,
            screen_bbox: List[int] = None,
            log_level: str = "info",
            network_retry: int = None,
            pause: [int, float] = None,
            timeout: [int, float] = None,
            max_match_number: int = None,
    ):
        return cls.find_image(
            *widget,
            rate=rate,
            multiple=multiple,
            picture_abspath=picture_abspath,
            screen_bbox=screen_bbox,
            log_level=log_level,
            network_retry=network_retry,
            pause=pause,
            timeout=timeout,
            max_match_number=max_match_number,
        )
