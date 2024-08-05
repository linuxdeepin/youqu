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
    ...

# 注意这里，只需要在这里挂一个装饰器
@log
class TestLog(BaseLog):
    """继承了基类BaseLog"""
    ...

    @staticmethod
    def static_method():
        """我是 类 里面的静态方法"""

        # 方法里面仍然可以单独打印日志
        logger.debug("这是我想再输出的其他 debug 日志")
        logger.info("这是我想再输出的其他 info 日志")
        logger.error("这是我想再输出的其他 error 日志")


if __name__ == '__main__':
    # @log装饰器自动打印
    TestLog().static_method()
