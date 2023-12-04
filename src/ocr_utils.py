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

from pdocr_rpc import OCR as _OCR
from pdocr_rpc.conf import setting as ocr_setting

from setting import conf

ocr_setting.PORT = conf.OCR_PORT
ocr_setting.SERVER_IP = conf.OCR_SERVER_HOST
ocr_setting.NETWORK_RETRY = int(conf.OCR_NETWORK_RETRY)
ocr_setting.PAUSE = float(conf.OCR_PAUSE)
ocr_setting.TIMEOUT = float(conf.OCR_TIMEOUT)
ocr_setting.MAX_MATCH_NUMBER = int(conf.OCR_MAX_MATCH_NUMBER)


class OCRUtils(_OCR):
    """OCR识别的工具类"""
