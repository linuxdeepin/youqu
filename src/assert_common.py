#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import os
from time import sleep
from typing import Union

try:
    import pyscreenshot
except ModuleNotFoundError:
    pass

from src.ocr_utils import OCRUtils as OCR
from src.image_utils import ImageUtils
from src.mouse_key import MouseKey
from src.filectl import FileCtl
from src.dogtail_utils import DogtailUtils
from src.custom_exception import TemplateElementNotFound
from src.custom_exception import TemplateElementFound
from src.custom_exception import ElementNotFound
from src.custom_exception import ElementExpressionError
from src.custom_exception import AssertOptionError
from src.cmdctl import CmdCtl
from src.button_center import ButtonCenter
from src import logger, log
from setting.globalconfig import GlobalConfig


@log
class AssertCommon:
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
        """
         期望界面存在模板图片
        :param widget: 图片路径 例：apps/autotest_app/assert_res/1.png
        :param rate: 匹配相似度
        """
        logger.info(f"屏幕上匹配图片< {f'***{widget[-40:]}' if len(widget) >= 40 else widget} >")

        try:
            ImageUtils.find_image(
                widget,
                rate=rate,
                multiple=multiple,
                picture_abspath=picture_abspath,
                network_retry=network_retry,
                pause=pause,
                timeout=timeout,
                max_match_number=match_number,
            )
        except TemplateElementNotFound as exc:
            raise AssertionError(exc) from TemplateElementNotFound
        except Exception as exc:
            raise AssertOptionError(exc) from Exception

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
        logger.info(f"屏幕上匹配图片< {f'***{widget[-40:]}' if len(widget) >= 40 else widget} >")
        try:
            ImageUtils.get_during(widget, screen_time, rate, pause)
        except TemplateElementNotFound as exc:
            raise AssertionError(exc) from TemplateElementNotFound
        except Exception as exc:
            raise AssertOptionError(exc) from Exception

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
        """
         期望界面不存在模板图片
        :param widget: 图片路径 apps/autotest_app/assert_res/1.png
        :param rate: 匹配相似度
        """
        logger.info(
            f"屏幕上匹配不存在图片< {f'***{widget[-40:]}' if len(widget) >= 40 else widget} >"
        )
        try:
            sleep(1)
            ImageUtils.find_image(
                widget,
                rate=rate,
                multiple=multiple,
                picture_abspath=picture_abspath,
                network_retry=network_retry,
                pause=pause,
                timeout=timeout,
                max_match_number=match_number,
            )
            raise TemplateElementFound(widget)
        except TemplateElementNotFound:
            pass
        except TemplateElementFound as exc:
            raise AssertionError(exc) from TemplateElementFound
        except Exception as exc:
            raise AssertOptionError(exc) from Exception

    @staticmethod
    def assert_file_exist(widget, file=None, recursive=False):
        """
         期望存在文件路径
        :param widget: 文件全路径或目录 例：~/Desktop/1.txt
        :param file: 文件名
        :param recursive: 是否递归查找
        """
        sleep(1)
        if recursive:
            if file:
                for _, _, files in os.walk(widget):
                    for filename in files:
                        if file == filename:
                            return True
                raise AssertionError(f"目录 {widget}及子目录无 {file} 文件")
            if not os.path.exists(os.path.expanduser(widget)):
                raise AssertionError(f"文件不存在！ 路径 {widget}")
            return True
        if file:
            _path = f"{widget}/{file}"
        else:
            _path = widget
        logger.info(f"断言文件存在<{_path}>")
        if not os.path.exists(os.path.expanduser(_path)):
            raise AssertionError(f"文件不存在！ 路径 {_path}")
        return True

    @staticmethod
    def assert_file_not_exist(widget, file=None, recursive=False):
        """
         期望不存在文件路径
        :param widget: 文件全路径 例：~/Desktop/1.txt
        :param file: 文件名
        :param recursive: 是否递归查找
        """
        sleep(1)
        logger.info(f"断言文件不存在<{widget}>")
        if recursive:
            if file:
                for _, _, files in os.walk(widget):
                    for filename in files:
                        if file == filename:
                            raise AssertionError(f"目录 {widget}或子目录存在 {file} 文件")
            else:
                if os.path.exists(os.path.expanduser(widget)):
                    raise AssertionError(f"文件存在！ 路径 {widget}")
        else:
            if file:
                widget = f"{widget}/{file}"
            if os.path.exists(os.path.expanduser(widget)):
                raise AssertionError(f"文件存在！ 路径 {widget}")

    @staticmethod
    def assert_element_exist(expr):
        """
         期望元素存在
        :param expr: 匹配元素的格式, 例如： $//dde-file-manager//1.txt
        """
        sleep(0.5)
        logger.info(f"断言元素存在<{expr}>")
        if not DogtailUtils().find_element_by_attr(expr):
            raise AssertionError(f"元素不存在！！！expr= <{expr}>")

    @staticmethod
    def assert_element_not_exist(expr):
        """
         期望元素不存在
        :param expr: 匹配元素的格式
        """
        logger.info(f"断言元素不存在<{expr}>")
        try:
            DogtailUtils().find_element_by_attr(expr)
            raise AssertionError(f"元素不应存在！！！expr= <{expr}>")
        except ElementNotFound:
            pass

    @staticmethod
    def assert_element_numbers(expr, number):
        """
         查找元素的个数与期望一致
        :param expr: 匹配元素的格式
        :param number: 匹配元素个数
        """
        logger.info(f"断言元素出现的个数 <{expr}, {number}>")
        result = DogtailUtils().find_elements_by_attr(expr)
        if isinstance(result, bool):
            raise ElementExpressionError(expr)
        if len(result) != number:
            raise AssertionError(f"元素个数{len(result)} 与期望个数 {number} 不符!")

    @staticmethod
    def assert_window_size(expect, real):
        """
         断言窗口大小与期望一致
        :param expect: 窗口的期望大小 （1920, 400）
        :param real: 窗口的实际大小（1920, 400）
        """
        logger.info(f"断言实际窗口大小{real}与期望{expect}是否相同")
        if expect != real:
            raise AssertionError(f"实际窗口大小{real}与期望{expect}不相同")

    @staticmethod
    def assert_process_status(expect, app):
        """
         断言应用进程是否存在
        :param expect: 进程期望结果 True /False
        :param app: 应用名字
        """
        logger.info(f"断言应用进程状态{app}与期望{expect}是否相同")
        if expect != CmdCtl.get_process_status(app):
            raise AssertionError(f"断言应用进程状态{app}与期望{expect}不相同")

    @staticmethod
    def assert_process_num(num, app):
        """
         断言应用进程的数量
        :param num: 期望的进程数量
        :param app: 应用名字
        """
        logger.info(f"断言 {app} 应用进程数量是否为 {num}")
        if num != CmdCtl.get_daemon_process_num(app):
            raise AssertionError(f"断言 {app} 应用进程数量与期望{num}不相同")

    @staticmethod
    def assert_window_amount(app, expect):
        """
         断言应用窗口数量
        :param expect: 应用窗口数量
        :param app: 应用名字
        """
        logger.info(f"断言应用窗口数量{app}与期望{expect}是否相同")
        number = ButtonCenter(app_name=app, config_path="xxx").get_windows_number(app)
        if expect != number:
            raise AssertionError(f"断言应用窗口数量{app}为{number}与期望{expect}不相同")

    @staticmethod
    def assert_share_folder(filename):
        """
         断言存在共享文件夹 filename
        :param filename: 共享文件夹名称
        """
        share_folder = CmdCtl.run_cmd(
            "net usershare list",
            interrupt=False,
            out_debug_flag=False,
            command_log=False,
        )
        if share_folder:
            share_folder = share_folder.split("\n")
        logger.info(f"断言共享目录中是否存在{filename}文件夹")
        if filename not in share_folder:
            raise AssertionError(f"断言共享目录中不存在{filename}文件夹")

    @staticmethod
    def assert_not_share_folder(filename):
        """
         断言不存在共享文件夹 filename
        :param filename: 共享文件夹名称
        """
        share_folder = CmdCtl.run_cmd(
            "net usershare list",
            interrupt=False,
            out_debug_flag=False,
            command_log=False,
        )
        if share_folder:
            share_folder = share_folder.split("\n")
        logger.info(f"断言共享目录中是否存在{filename}文件夹")
        if filename in share_folder:
            raise AssertionError(f"断言共享目录中存在{filename}文件夹")

    @staticmethod
    def assert_theme(expect):
        """
         断言主题, 图片中颜色大于50%, 为断言主题准确性，建议最大化窗口
        :param expect: 期望的主题 浅色/深色
        """
        logger.info(f"断言主题是否为<{expect}>主题")
        config = {"浅色": (248, 248, 248), "深色": (37, 37, 37)}
        exp_color = config[expect]
        # 在data/pic_res这个目录下生成一张临时的图，每次生成会被覆盖
        if GlobalConfig.IS_X11:
            pyscreenshot.grab().save(GlobalConfig.SCREEN_CACHE)
        else:
            GlobalConfig.SCREEN_CACHE = (
                os.popen("qdbus org.kde.KWin /Screenshot screenshotFullscreen").read().strip("\n")
            )
        color_list = ImageUtils.find_image_color(GlobalConfig.SCREEN_CACHE)
        proportion = round(color_list.count(exp_color) / len(color_list), 2)
        if proportion < 0.6:
            raise AssertionError(
                f"{expect}主题颜色占屏幕总体颜色占比低于60%，实际占比{proportion * 100}%，初步断言主题失败"
            )

    @staticmethod
    def assert_equal(expect, actual):
        """
         断言相等
        :param expect: 期望结果
        :param actual: 实际结果
        """
        logger.info(f"预期值<{expect}>与实际值<{actual}>是否相等")
        if not bool(expect == actual):
            raise AssertionError(f"预期值<{expect}>与实际值<{actual}>不相等")

    @staticmethod
    def assert_not_equal(expect, actual):
        """
         断言不相等
        :param expect: 期望结果
        :param actual: 实际结果
        """
        logger.info(f"预期值<{expect}>与实际值<{actual}>是否相等")
        if bool(expect == actual):
            raise AssertionError(f"预期值<{expect}>与实际值<{actual}>不相等")

    @staticmethod
    def assert_true(expect):
        """
         断言结果为真
        :param expect: 结果
        """
        if not expect:
            raise AssertionError(f"<{expect}>不为真")

    @staticmethod
    def assert_false(expect):
        """
         断言结果为假
        :param expect: 结果
        """
        if expect:
            raise AssertionError(f"<{expect}>不为假")

    @classmethod
    def assert_pic_px(cls, file, size=(0, 0)):
        """
         断言图片尺寸
        :param file: 结果
        :param size: 期望尺寸 例如（120, 400）
        """
        really = ImageUtils.get_pic_px(file)
        if size != really:
            raise AssertionError(f"实际尺寸<{really}>与期望尺寸<{size}>不符")

    @classmethod
    def assert_file_endwith_exist(cls, path, endwith):
        """
         断言路径下是否存在以 endwith 结果的文件
        :param path: 路径
        :param endwith: 文件后缀， txt，rar 等
        """
        if not FileCtl.find_files(path, endwith=endwith):
            raise AssertionError(f"路径 {path} 下，不存在以 {endwith} 结尾的文件")

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
        :param args: 目标字符,识别一个字符串或多个字符串。
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
                注意 ： end_x + end_y 与 w + h 为互斥关系, 必须且只能传入其中一组
            示例：
                {start_x=0， start_y=0， w=100， h=100}
                {start_x=0， start_y=0， end_x=100， end_y=100}
        """

        if len(args) == 0:
            raise ValueError("缺少 ocr 断言关键字")

        pic = None
        if picture_abspath is not None:
            pic = picture_abspath + ".png"

        resolution = MouseKey.screen_size()
        if bbox is not None:
            start_x = bbox.get("start_x") if bbox.get("start_x") is not None else None
            start_y = bbox.get("start_y") if bbox.get("start_y") is not None else None
            w = bbox.get("w") if bbox.get("w") is not None else None
            h = bbox.get("h") if bbox.get("h") is not None else None
            end_x = bbox.get("end_x") if bbox.get("end_x") is not None else None
            end_y = bbox.get("end_y") if bbox.get("end_y") is not None else None

            if start_x is None or start_y is None:
                raise ValueError("缺失 start_x 或 start_y 坐标")

            wh_provided = w is not None and h is not None
            end_xy_provided = end_x is not None and end_y is not None

            if not (wh_provided ^ end_xy_provided):
                raise ValueError("end_x + end_y 与 w + h 为互斥关系, 必须且只能传入其中一组")

            if end_xy_provided:
                w = end_x - start_x
                h = end_y - start_y
            picture_abspath = ImageUtils.save_temporary_picture(start_x, start_y, w, h)
            pic = picture_abspath + ".png"

            resolution = f"{start_x, start_y} -> {w, h}"

        res = OCR.ocr(
            *args,
            picture_abspath=pic,
            similarity=similarity,
            return_first=return_first,
            lang=lang,
            network_retry=network_retry,
            pause=pause,
            timeout=timeout,
            max_match_number=max_match_number,
        )
        if res is False:
            raise AssertionError(
                (
                    f"通过OCR在范围[{resolution}]未识别到：{args}",
                    f"{pic if pic else GlobalConfig.SCREEN_CACHE}",
                )
            )
        if isinstance(res, tuple):
            pass
        elif isinstance(res, dict):
            mode = mode.lower()
            if mode == "all" and False in res.values():
                res = filter(lambda x: x[1] is False, res.items())
                raise AssertionError(
                    (
                        f"通过OCR在范围[{resolution}]未识别到：{dict(res)}",
                        f"{pic if pic else GlobalConfig.SCREEN_CACHE}",
                    )
                )
            elif mode == "any" and len(res) == list(res.values()).count(False):
                raise AssertionError(
                    (
                        f"通过OCR在范围[{resolution}]未识别到：{args}中的任意一个",
                        f"{pic if pic else GlobalConfig.SCREEN_CACHE}",
                    )
                )

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
        """
        断言文案不存在
        :param args: 目标字符,识别一个字符串或多个字符串。
        :param picture_abspath: 要识别的图片路径，如果不传默认截取全屏识别。
        :param similarity: 匹配度。
        :param return_first: 只返回第一个,默认为 False,返回识别到的所有数据。
        :param lang: `ch`, `en`, `fr`, `german`, `korean`, `japan`
        :param network_retry: 连接服务器重试次数
        :param pause: 重试间隔时间,单位秒
        :param timeout: 最大匹配超时,单位秒
        :param max_match_number: 最大匹配次数
        :param bbox:
            接收一个字典，包含一个区域，在区域内进行识别，用于干扰较大时提升OCR识别精准度
            字典字段:
                start_x: 开始 x 坐标（左上角）
                start_y: 开始 y 坐标（左上角）
                w: 宽度
                h: 高度
                end_x: 结束 x 坐标（右下角）
                end_y: 结束 y 坐标（右下角）
                注意 ： end_x + end_y 与 w + h 为互斥关系, 必须且只能传入其中一组
            示例：
                {start_x=0， start_y=0， w=100， h=100}
                {start_x=0， start_y=0， end_x=100， end_y=100}
        """

        if len(args) == 0:
            raise ValueError("缺少 ocr 断言关键字")

        pic = None
        if picture_abspath is not None:
            pic = picture_abspath + ".png"

        resolution = MouseKey.screen_size()
        if bbox is not None:
            start_x = bbox.get("start_x") if bbox.get("start_x") is not None else None
            start_y = bbox.get("start_y") if bbox.get("start_y") is not None else None
            w = bbox.get("w") if bbox.get("w") is not None else None
            h = bbox.get("h") if bbox.get("h") is not None else None
            end_x = bbox.get("end_x") if bbox.get("end_x") is not None else None
            end_y = bbox.get("end_y") if bbox.get("end_y") is not None else None

            if start_x is None or start_y is None:
                raise ValueError("缺失 start_x 或 start_y 坐标")

            wh_provided = w is not None and h is not None
            end_xy_provided = end_x is not None and end_y is not None

            if not (wh_provided ^ end_xy_provided):
                raise ValueError("end_x + end_y 与 w + h 为互斥关系, 必须且只能传入其中一组")

            if end_xy_provided:
                w = end_x - start_x
                h = end_y - start_y
            picture_abspath = ImageUtils.save_temporary_picture(start_x, start_y, w, h)
            pic = picture_abspath + ".png"

            resolution = f"{start_x, start_y} -> {w, h}"

        res = OCR.ocr(
            *args,
            picture_abspath=pic,
            similarity=similarity,
            return_first=return_first,
            lang=lang,
            network_retry=network_retry,
            pause=pause,
            timeout=timeout,
            max_match_number=max_match_number,
        )
        if res is False:
            pass
        elif isinstance(res, tuple):
            raise AssertionError(
                (
                    f"通过ocr在范围[{resolution}]识别到不应存在的文案 {res}",
                    f"{pic if pic else GlobalConfig.SCREEN_CACHE}",
                )
            )
        elif isinstance(res, dict):
            if all(value is False for value in res.values()):
                pass
            else:
                res = filter(lambda x: x[1] is not False, res.items())
                raise AssertionError(
                    (
                        f"通过OCR在范围[{resolution}]识别到不应存在的文案：{dict(res)}",
                        f"{pic if pic else GlobalConfig.SCREEN_CACHE}",
                    )
                )
