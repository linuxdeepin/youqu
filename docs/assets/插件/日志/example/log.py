#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: Apache Software License
from funnylog import logger
from funnylog import log
from funnylog.conf import setting

setting.CLASS_NAME_ENDSWITH = ("Log",)
logger("DEBUG")


class BaseLog:

    def base_self_method(self):
        """我是 基类 里面的实例方法"""

    @classmethod
    def base_cls_method(self):
        """我是 基类 里面的类方法"""

    @staticmethod
    def base_static_method():
        """我是 基类 里面的静态方法"""

# 注意这里，只需要在这里挂一个装饰器
@log
class TestLog(BaseLog):
    """继承了基类BaseLog"""

    def self_method(self):
        """我是 类 里面的实例方法"""

    @classmethod
    def cls_method(self):
        """我是 类 里面的类方法"""

    @staticmethod
    def static_method():
        """我是 类 里面的静态方法"""


if __name__ == '__main__':
    # @log装饰器自动打印
    TestLog().self_method()
    TestLog().cls_method()
    TestLog().static_method()
    # 直接调用基类里面的方法，也能自动打印
    TestLog().base_self_method()
    TestLog().base_cls_method()
    TestLog().base_static_method()
