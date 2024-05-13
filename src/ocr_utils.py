#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
# pylint: disable=E0401,C0413,R0903,W0707,W0611
import random

from pdocr_rpc import OCR as _OCR
from pdocr_rpc.conf import setting as ocr_setting

from setting import conf

ocr_setting.PORT = conf.OCR_PORT
ocr_setting.SERVER_IP = conf.OCR_SERVER_HOST
ocr_setting.NETWORK_RETRY = int(conf.OCR_NETWORK_RETRY)
ocr_setting.PAUSE = float(conf.OCR_PAUSE)
ocr_setting.TIMEOUT = float(conf.OCR_TIMEOUT)
ocr_setting.MAX_MATCH_NUMBER = int(conf.OCR_MAX_MATCH_NUMBER)


class OCRUtils:
    ocr_setting.NETWORK_RETRY = int(conf.OCR_NETWORK_RETRY)
    ocr_setting.PAUSE = float(conf.OCR_PAUSE)
    ocr_setting.TIMEOUT = float(conf.OCR_TIMEOUT)
    ocr_setting.MAX_MATCH_NUMBER = int(conf.OCR_MAX_MATCH_NUMBER)
    ocr_setting.PORT = conf.OCR_PORT
    ocr_servers = [i.strip() for i in conf.OCR_SERVER_HOST.split("/") if i]
    x = None
    y = None
    result = None

    @classmethod
    def ocr(cls, *args, **kwargs):
        """ocr load balance"""
        servers = cls.ocr_servers
        while servers:
            ocr_setting.SERVER_IP = random.choice(servers)
            if _OCR.check_connected() is False:
                servers.remove(ocr_setting.SERVER_IP)
                ocr_setting.SERVER_IP = None
            else:
                break
        if ocr_setting.SERVER_IP is None:
            raise EnvironmentError(f"所有OCR服务器不可用: {cls.ocr_servers}")
        result = _OCR.ocr(*args, **kwargs)
        return result

    @classmethod
    def ocrx(cls, *args, **kwargs):
        cls.result = cls.ocr(*args, **kwargs)
        if isinstance(cls.result, tuple):
            cls.x, cls.y = cls.result
            return cls
        return cls.result

    @classmethod
    def click(cls):
        from src.mouse_key import MouseKey
        if cls.x is None and cls.y is None:
            raise ValueError("ocr_pro 没有识别到")
        MouseKey.click(cls.x, cls.y)
        return cls

    @classmethod
    def right_click(cls):
        from src.mouse_key import MouseKey
        if cls.x is None and cls.y is None:
            raise ValueError("ocr_pro 没有识别到")
        MouseKey.right_click(cls.x, cls.y)
        return cls

    @classmethod
    def double_click(cls):
        from src.mouse_key import MouseKey
        if cls.x is None and cls.y is None:
            raise ValueError("ocr_pro 没有识别到")
        MouseKey.double_click(cls.x, cls.y)
        return cls

    @classmethod
    def center(cls):
        if cls.x is None and cls.y is None:
            raise ValueError("ocr_pro 没有识别到")
        return cls.x, cls.y

    @classmethod
    def all_result(cls):
        return cls.result


if __name__ == '__main__':
    OCRUtils.ocrx().click()
