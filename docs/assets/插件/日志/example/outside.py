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


if __name__ == '__main__':
    # logger直接调用
    logger.debug("这是在类外面打 debug log")
    logger.info("这是在类外面打 info log")
    logger.error("这是在类外面打 error log")
