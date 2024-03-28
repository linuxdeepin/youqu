#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only

import weakref
import threading


class Singleton(type):
    """底层单例模式封装"""

    _instance_lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Singleton.__instance = None
        # 初始化存放实例地址
        self._cache = weakref.WeakValueDictionary()

    def __call__(self, *args, **kwargs):
        # 提取类初始化时的参数
        kargs = "".join([f"{key}" for key in args]) if args else ""
        kkwargs = "".join([f"{key}" for key in kwargs]) if kwargs else ""
        # 判断相同参数的实例师否被创建
        if kargs + kkwargs not in self._cache:  # 存在则从内存地址中取实例
            with Singleton._instance_lock:
                Singleton.__instance = super().__call__(*args, **kwargs)
                self._cache[kargs + kkwargs] = Singleton.__instance
        # 不存在则新建实例
        else:
            Singleton.__instance = self._cache[kargs + kkwargs]
        return Singleton.__instance
