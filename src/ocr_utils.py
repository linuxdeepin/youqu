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
    def _check_xy(cls):
        if cls.x is None and cls.y is None:
            raise ValueError("ocrx 没有识别到")

    @classmethod
    def click(cls):
        from src.mouse_key import MouseKey
        cls._check_xy()
        MouseKey.click(cls.x, cls.y)
        return cls

    @classmethod
    def right_click(cls):
        from src.mouse_key import MouseKey
        cls._check_xy()
        MouseKey.right_click(cls.x, cls.y)
        return cls

    @classmethod
    def double_click(cls):
        from src.mouse_key import MouseKey
        cls._check_xy()
        MouseKey.double_click(cls.x, cls.y)
        return cls

    @classmethod
    def center(cls):
        cls._check_xy()
        return cls.x, cls.y

    @classmethod
    def all_result(cls):
        return cls.result

    @classmethod
    def ocr_find_by_range(cls, text, x1=0, x2=1920, y1=0, y2=1080):
        """
        OCR在界面中识别到多个关键词时，通过区域筛选出对应关键词并返回坐标
        :param text: 页面查找关键词
        :param x1: x坐标开始范围
        :param x2: x坐标结束范围
        :param y1: y坐标开始范围
        :param y2: y坐标结束范围
        :return: 坐标 x, y
        """
        ocr_return = cls.ocr(text)
        if isinstance(ocr_return, tuple):
            return ocr_return[0], ocr_return[1]
        elif isinstance(ocr_return, dict):
            for key, value in ocr_return.items():
                if x1 <= value[0] <= x2 and y1 <= value[1] <= y2:
                    return value[0], value[1]


if __name__ == '__main__':
    OCRUtils.ocrx().click()
