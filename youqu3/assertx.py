#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import os
from funnylog2.config import config as funnylog2_config
from typing import Union
from youqu3 import exceptions
from youqu3 import log, logger, setting
from youqu3.cmd import Cmd

funnylog2_config.CLASS_NAME_ENDSWITH.append("Assert")


@log
class Assert:
    """
    自定义断言类
    """

    @staticmethod
    def assert_image_exist(
        widget: str,
        rate: float = None,
        multiple: bool = False,
        picture_abspath: str = None,
        network_retry: int = None,
        pause: [int, float] = None,
        timeout: [int, float] = None,
        match_number: int = None,
    ):
        """判断界面存在{{widget}}模板图片"""
        from youqu3.gui import pylinuxauto

        try:
            pylinuxauto.find_element_by_image(
                widget,
                rate=rate,
                multiple=multiple,
                picture_abspath=picture_abspath,
                network_retry=network_retry,
                pause=pause,
                timeout=timeout,
                max_match_number=match_number,
            )
        except pylinuxauto.exceptions.TemplateElementNotFound as exc:
            raise AssertionError(
                exc
            ) from pylinuxauto.exceptions.TemplateElementNotFound

    @staticmethod
    def assert_image_not_exist(
        widget: str,
        rate: float = None,
        multiple: bool = False,
        picture_abspath: str = None,
        network_retry: int = None,
        pause: [int, float] = None,
        timeout: [int, float] = None,
        match_number: int = None,
    ):
        """判断界面不存在{{widget}}模板图片"""
        from youqu3.gui import pylinuxauto

        try:
            pylinuxauto.find_element_by_image(
                widget,
                rate=rate,
                multiple=multiple,
                picture_abspath=picture_abspath,
                network_retry=network_retry,
                pause=pause,
                timeout=timeout,
                max_match_number=match_number,
            )
            raise exceptions.TemplateElementFound(widget)
        except pylinuxauto.exceptions.TemplateElementNotFound:
            ...

    @classmethod
    def assert_image_exist_during_time(
        cls,
        widget: str,
        screen_time: Union[float, int],
        rate: float = None,
        pause: Union[int, float] = None,
    ):
        """
        在一段时间内截图多张图片进行识别，其中有一张图片识别成功即返回结果;
        适用于气泡类的断言，比如气泡在1秒内消失，如果用常规的图像识别则有可能无法识别到；
        :param image_path: 要识别的模板图片；
        :param screen_time: 截取屏幕图片的时间，单位秒；
        :param rate: 识别率；
        :param pause: 截取屏幕图片的间隔时间，默认不间隔；
        """
        logger.info(
            f"屏幕上匹配图片< {f'***{widget[-40:]}' if len(widget) >= 40 else widget} >"
        )
        from youqu3.gui import pylinuxauto

        try:
            pylinuxauto.get_during(widget, screen_time, rate, pause)
        except exceptions.TemplateElementNotFound as exc:
            raise AssertionError(exc) from exceptions.TemplateElementNotFound

    @staticmethod
    def assert_file_exist(file_path):
        """判断文件{{file_path}}存在"""
        if not os.path.exists(os.path.expanduser(file_path)):
            raise AssertionError(f"文件{file_path}不存在")
        return True

    @staticmethod
    def assert_file_not_exist(file_path):
        """判断文件{{file_path}}不存在"""
        if os.path.exists(os.path.expanduser(file_path)):
            raise AssertionError(f"文件{file_path}存在")

    @staticmethod
    def assert_element_exist(expr):
        """判断元素{{expr}}存在"""
        from youqu3.gui import pylinuxauto

        try:
            pylinuxauto.find_element_by_attr_path(expr)
        except pylinuxauto.exceptions.ElementNotFound:
            raise exceptions.ElementNotFound(expr)

    @staticmethod
    def assert_element_not_exist(expr):
        """判断元素{{expr}}不存在"""
        from youqu3.gui import pylinuxauto

        try:
            pylinuxauto.find_element_by_attr_path(expr)
            raise exceptions.ElementFound(expr)
        except pylinuxauto.exceptions.ElementNotFound:
            pass

    @staticmethod
    def assert_equal(expect, actual):
        """判断预期值<{{expect}>与实际值<{{actual}>相等"""
        if expect != actual:
            raise AssertionError(f"预期值<{expect}>与实际值<{actual}>不相等")

    @staticmethod
    def assert_not_equal(expect, actual):
        """判断预期值<{{expect}>与实际值<{{actual}>不相等"""
        if expect == actual:
            raise AssertionError(f"预期值<{expect}>与实际值<{actual}>相等")

    @staticmethod
    def assert_in(target: str, pool: str):
        """判断<{{target}}>在<{{pool}}>中"""
        if target not in pool:
            raise AssertionError(f"<{target}>不在<{pool}>中")

    @staticmethod
    def assert_not_in(target: str, pool: str):
        """判断<{{target}}>不在<{{pool}}>中"""
        if target in pool:
            raise AssertionError(f"<{target}>在<{pool}>中")

    @staticmethod
    def assert_sequence_in(target: list, pool: list):
        """判断<{{target}}>在<{{pool}}>中"""
        for i in target:
            if i not in pool:
                raise AssertionError(f"{pool}中不存在{i}")

    @staticmethod
    def assert_sequence_not_in(target: list, pool: list):
        """判断<{{target}}>不在<{{pool}}>中"""
        for i in target:
            if i in pool:
                raise AssertionError(f"{pool}中存在{i}")

    @staticmethod
    def assert_true(expect):
        """断言{{expect}}结果为真"""
        if not expect:
            raise AssertionError(f"<{expect}>不为真")

    @staticmethod
    def assert_false(expect):
        """断言{{expect}}结果为假"""
        if expect:
            raise AssertionError(f"<{expect}>不为假")

    @staticmethod
    def assert_any(expect):
        """断言任一{{expect}}结果为真"""
        if not any(expect):
            raise AssertionError(f"<{expect}>均不为真")

    @staticmethod
    def assert_all(expect):
        """断言所有{{expect}}结果为真"""
        if not all(expect):
            raise AssertionError(f"<{expect}>不均为真")

    @staticmethod
    def assert_ocr_exist(
        *args,
        picture_abspath=None,
        similarity=0.6,
        return_first=False,
        lang="ch",
        network_retry: int = None,
        pause: [int, float] = None,
        timeout: [int, float] = None,
        max_match_number: int = None,
        mode: str = "all",
        bbox: dict = None,
    ):
        """
        断言文案存在
        :param args:
            目标字符,识别一个字符串或多个字符串,并返回其在图片中的坐标;
            如果不传参，返回图片中识别到的所有字符串。
        :param picture_abspath: 要识别的图片路径，如果不传默认截取全屏识别。
        :param similarity: 匹配度。
        :param return_first: 只返回第一个,默认为 False,返回识别到的所有数据。
        :param lang: `ch`, `en`, `fr`, `german`, `korean`, `japan`
        :param network_retry: 连接服务器重试次数
        :param pause: 重试间隔时间,单位秒
        :param timeout: 最大匹配超时,单位秒
        :param max_match_number: 最大匹配次数
        :param mode: "all" or "any"，all 表示识别所有目标字符，any 表示识别任意一个目标字符，默认值为 all
        :param bbox:
            接收一个字典，包含一个区域，在区域内进行识别，用于干扰较大时提升OCR识别精准度
            字典字段:
                start_x: 开始 x 坐标（左上角）
                start_y: 开始 y 坐标（左上角）
                w: 宽度
                h: 高度
                end_x: 结束 x 坐标（右下角）
                end_y: 结束 y 坐标（右下角）
                return_one: True/False（默认为True）
                注意 ：
                    1、end_x + end_y 与 w + h 为互斥关系, 必须且只能传入其中一组
                    2、加入此参数后代表范围内只能出现唯一坐标则通过，若必须返回多组坐标可修改'return_one'的值
                示例：
                {"start_x": 0, "start_y": 0, "w": 100, "h": 100}
                {"start_x": 0, "start_y": 0, "end_x": 100, "end_y": 100}
        """
        if len(args) == 0:
            raise ValueError("缺少 ocr 断言关键字")

        pic = None
        if picture_abspath is not None:
            pic = picture_abspath

        from youqu3.gui import pylinuxauto
        from youqu3.gui import pylinuxauto_config

        res = pylinuxauto.find_element_by_ocr(
            *args,
            picture_abspath=pic,
            similarity=similarity,
            return_first=return_first,
            lang=lang,
            network_retry=network_retry,
            pause=pause,
            timeout=timeout,
            max_match_number=max_match_number,
            bbox=bbox,
        )
        if res.result is False:
            raise AssertionError(
                (
                    f"通过OCR未识别到：{args}",
                    f"{pic if pic else pylinuxauto_config.SCREEN_CACHE}",
                )
            )
        else:
            if isinstance(res.result, tuple):
                pass
            elif isinstance(res.result, dict):
                mode = mode.lower()
                if mode == "all" and False in res.result.values():
                    res = filter(lambda x: x[1] is False, res.result.items())
                    raise AssertionError(
                        (
                            f"通过OCR未识别到：{dict(res)} <- {args}",
                            f"{pic if pic else pylinuxauto_config.SCREEN_CACHE}",
                        )
                    )
                elif mode == "any" and len(res.result) == list(
                    res.result.values()
                ).count(False):
                    raise AssertionError(
                        (
                            f"通过OCR未识别到：{args}中的任意一个",
                            f"{pic if pic else pylinuxauto_config.SCREEN_CACHE}",
                        )
                    )
                else:
                    if bbox is not None:
                        if bbox.get("return_one") is True:
                            new_res = {}
                            for key, value in res.items():
                                new_res[key] = (
                                    value[0] + bbox.get("start_x"),
                                    value[1] + bbox.get("start_y"),
                                )
                            raise AssertionError(
                                f"传入bbox参数，范围内关键词非唯一：{new_res}"
                            )
                        elif bbox.get("return_one") is False:
                            pass

    @staticmethod
    def assert_ocr_not_exist(
        *args,
        picture_abspath=None,
        similarity=0.6,
        return_first=False,
        lang="ch",
        network_retry: int = None,
        pause: [int, float] = None,
        timeout: [int, float] = None,
        max_match_number: int = None,
        bbox: dict = None,
    ):
        """断言文案不存在"""
        if len(args) == 0:
            raise ValueError("缺少 ocr 断言关键字")

        pic = None
        if picture_abspath is not None:
            pic = picture_abspath

        from youqu3.gui import pylinuxauto
        from youqu3.gui import pylinuxauto_config

        res = pylinuxauto.find_element_by_ocr(
            *args,
            picture_abspath=pic,
            similarity=similarity,
            return_first=return_first,
            lang=lang,
            network_retry=network_retry,
            pause=pause,
            timeout=timeout,
            max_match_number=max_match_number,
            bbox=bbox,
        )
        print(res.result)
        if res.result is False:
            pass
        elif isinstance(res.result, tuple):
            raise AssertionError(
                (
                    f"通过ocr识别到不应存在的文案 {args} -> {res.result}",
                    f"{pic if pic else pylinuxauto_config.SCREEN_CACHE}",
                )
            )
        elif isinstance(res.result, dict):
            if all(value is False for value in res.result.values()):
                pass
            else:
                if bbox is not None:
                    new_res = {}
                    for key, value in res.result.items():
                        if isinstance(value, tuple):
                            new_res[key] = (
                                value[0] + bbox.get("start_x"),
                                value[1] + bbox.get("start_y"),
                            )
                        else:
                            new_res[key] = value
                else:
                    new_res = res.result
                raise AssertionError(
                    (
                        f"通过OCR识别到不应存在的文案：{args} -> {dict(new_res)}",
                        f"{pic if pic else pylinuxauto_config.SCREEN_CACHE}",
                    )
                )
