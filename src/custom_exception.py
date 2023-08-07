#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
# pylint: disable=W0707,W0611
try:
    from image_center import TemplateElementNotFound
    from image_center import TemplatePictureNotExist
except ImportError:
    raise ModuleNotFoundError

from src import logger


class ApplicationStartError(BaseException):
    """
    应用程序未启动
    """

    def __init__(self, result):
        """
        应用程序未启动
        :param result: 结果
        """
        err = f"应用程序未启动,{result}"
        logger.error(err)
        BaseException.__init__(self, err)


class ApplicationError(BaseException):
    """应用程序错误"""

    def __init__(self, msg):
        """
        应用程序错误
        :param msg: 结果
        """
        logger.error(msg)
        BaseException.__init__(self, msg)


class ElementNotFound(BaseException):
    """未找到元素"""

    def __init__(self, name):
        """
        未找到元素
        :param name: 命令
        """
        err = f"====未找到“{name}”元素！===="
        logger.error(err)
        BaseException.__init__(self, err)


# class TemplateElementNotFound(BaseException):
#     """通过模板资源未匹配到对应元素"""
#
#     def __init__(self, *name):
#         """
#         通过模板资源未匹配到对应元素
#         :param name: 命令
#         """
#         err = "通过图片资源, 未在屏幕上匹配到元素"
#         template = [f"{i}.png" for i in name]
#         BaseException.__init__(self, err, *template)


class TemplateElementFound(BaseException):
    """通过模板资源匹配到对应元素"""

    def __init__(self, *name):
        """
        通过模板资源匹配到对应元素
        :param name: 命令
        """
        err = "通过图片资源, 在屏幕中匹配到了不应该出现的元素"
        template = [f"{i}.png" for i in name]
        BaseException.__init__(self, err, *template)


# class TemplatePictureNotExist(BaseException):
#     """图片资源，文件不存在"""
#
#     def __init__(self, name):
#         """
#         文件不存在
#         :param name: 命令
#         """
#         err = f"图片资源：{name} 文件不存在!"
#         logger.error(err)
#         BaseException.__init__(self, err)


class AssertOptionError(AssertionError):
    """断言操作失败"""

    def __init__(self, e):
        """
        断言操作失败
        """
        err = f"断言操作失败，未知原因：{e}"
        logger.error(err)
        AssertionError.__init__(self, err)


class ParamError(BaseException):
    """参数错误"""

    def __init__(self, name, msg):
        """
        参数错误
        :param name: 命令
        """
        err = f"参数错误：{name}、\n{msg}"
        logger.error(err)
        BaseException.__init__(self, err)


class NoIconOfThisSize(BaseException):
    """没有操作的选项"""

    def __init__(self, size):
        """
        参数错误
        :param size:
        """
        err = f"参数错误：{size}"
        logger.error(err)
        BaseException.__init__(self, err)


class NoSuchWindowPositionParameter(BaseException):
    """没有此窗口位置参数"""

    def __init__(self, size):
        """
        参数错误
        :param size:
        """
        err = f"参数错误：{size}, 没有此窗口位置参数"
        logger.error(err)
        BaseException.__init__(self, err)


class GetWindowInformation(BaseException):
    """获取窗口信息错误"""

    def __init__(self, msg):
        """
        获取窗口信息错误
        """
        logger.error(msg)
        BaseException.__init__(self, msg)


class NoSetReferencePoint(BaseException):
    """没有设置参考点"""

    def __init__(self, msg):
        err = f"没有设置参考点！| {msg}"
        logger.error(err)
        BaseException.__init__(self, err)


class ShellExecutionFailed(BaseException):
    """shell执行失败"""

    def __init__(self, msg):
        err = f"shell执行失败！| {msg}"
        logger.error(err)
        BaseException.__init__(self, err)


class ElementExpressionError(BaseException):
    """查找元素表达式错误"""

    def __init__(self, msg):
        err = f"查找元素表达式错误 <{msg}>"
        logger.error(err)
        BaseException.__init__(self, err)


class NoSuchSkipMethodFound(BaseException):
    """未找到判断是否跳过的自定义方法"""

    def __init__(self, msg):
        err = f"未找到判断是否跳过的自定义方法 <{msg}>"
        logger.error(err)
        BaseException.__init__(self, err)


class OcrTextRecognitionError(BaseException):
    """Ocr文字识别失败"""

    def __init__(self, msg):
        err = f"Ocr文字识别失败 <{msg}>"
        logger.error(err)
        BaseException.__init__(self, err)
