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
    def ocr_remote(
            cls,
            target_strings: tuple = None,
            picture_abspath: str = None,
            similarity: [int, float] = 0.6,
            return_default: bool = False,
            return_first: bool = False,
            lang: str = "ch",
            network_retry: int = None,
            pause: [int, float] = None,
            timeout: [int, float] = None,
            max_match_number: int = None,
    ):
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
        return _OCR.ocr(
            *target_strings,
            picture_abspath=picture_abspath,
            similarity=similarity,
            return_default=return_default,
            return_first=return_first,
            lang=lang,
            network_retry=network_retry,
            pause=pause,
            timeout=timeout,
            max_match_number=max_match_number,
        )

    @classmethod
    def ocrx(cls, *args, **kwargs):
        """
        支持链式调用
        ocrx().click()
        """
        cls.result = cls.ocr(*args, **kwargs)
        if isinstance(cls.result, tuple):
            cls.x, cls.y = cls.result
            return cls
        return cls.result

    @classmethod
    def check_xy(cls):
        if cls.x is None and cls.y is None:
            raise ValueError("ocr_pro 没有识别到")

    @classmethod
    def click(cls):
        from src.mouse_key import MouseKey
        cls.check_xy()
        MouseKey.click(cls.x, cls.y)
        return cls

    @classmethod
    def right_click(cls):
        from src.mouse_key import MouseKey
        cls.check_xy()
        MouseKey.right_click(cls.x, cls.y)
        return cls

    @classmethod
    def double_click(cls):
        from src.mouse_key import MouseKey
        cls.check_xy()
        MouseKey.double_click(cls.x, cls.y)
        return cls

    @classmethod
    def center(cls):
        cls.check_xy()
        return cls.x, cls.y

    @classmethod
    def all_result(cls):
        return cls.result


if __name__ == '__main__':
    OCRUtils.ocrx().click()
