#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
from xmlrpc.client import ServerProxy

from setting.globalconfig import GlobalConfig

try:
    import pypinyin

    GET_PINYIN_FROM_RPC = False
except ModuleNotFoundError:
    GET_PINYIN_FROM_RPC = True


def pinyin(word) -> str:
    """
     汉字转化为拼音
    :param word: 待转化的汉语字符串
    :return: 拼音字符串
    """
    if GET_PINYIN_FROM_RPC:
        server = ServerProxy(GlobalConfig.OPENCV_SERVER_HOST, allow_none=True)
        return server.pinyin(word)
    # else:
    _s = ""
    for key in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        _s += "".join(key)
    return _s
