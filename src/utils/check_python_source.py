#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
from urllib import request
from urllib import parse
from urllib.error import URLError
from urllib.request import build_opener
from http import cookiejar


class RequestX:
    """RequestX"""

    def __init__(
        self,
        login_url=None,
        headers=None,
        data=None,
    ):
        self.login_url = login_url
        self.headers = headers
        self.data = parse.urlencode(data).encode("utf-8") if data else None
        self.kwargs = {}
        if self.login_url:
            self.kwargs["url"] = self.login_url
        if self.headers:
            self.kwargs["headers"] = self.headers
        if self.data:
            self.kwargs["data"] = self.data

    @property
    def session(self):
        """
         获取opener对象
        :return:
        """
        cookie_jar = cookiejar.CookieJar()
        cookie = request.HTTPCookieProcessor(cookie_jar)
        opener = build_opener(cookie)
        if self.login_url:
            requests = request.Request(**self.kwargs)
            opener.open(requests)
        return opener

    def open_url(self, url, data=None):
        """
         访问url
        :param url:
        :return:
        """
        response = self.session.open(url, data=data, timeout=2)
        return response


if __name__ == "__main__":
    rx = RequestX()
    CODE = 201
    try:
        CODE = rx.open_url("https://it.uniontech.com").code
    except URLError:
        pass
    print(CODE, end="")
