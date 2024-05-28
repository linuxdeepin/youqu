#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
from http import cookiejar
from urllib import parse
from urllib import request
from urllib.request import build_opener
import json as _json


class RequestX:
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

    def open_url(self, url, data=None, timeout=None):
        """
         访问url
        :param url:
        :return:
        """
        if timeout is None:
            timeout = object()
        response = self.session.open(url, data=data, timeout=timeout).read().decode()
        return response

    @classmethod
    def post(cls, url: str, headers: dict, data: dict = None, json: dict=None):
        if data:
            params = parse.urlencode(data).encode("utf-8")
        elif json:
            params = _json.dumps(json)
            params = bytes(params, "utf-8")
        else:
            raise ValueError
        r = request.Request(url=url, data=params, headers=headers, method="POST")
        req = request.urlopen(r).read().decode("utf-8")
        return req


if __name__ == "__main__":
    user = ""  # 工号
    password = ""  # 密码
    login_url = "https://pms.uniontech.com/user-login-Lw==.html"
    headers = {"content-type": "application/x-www-form-urlencoded; charset=UTF-8"}
    data = {
        "account": user,
        "password": password,
        "passwordStrength": "1",
        "referer": "/zentao/",
        "verifyRand": "370729017",
        "keepLogin": "0",
    }
    # rx = RequestX(login_url=login_url, headers=headers, data=data)
    # url = "https://pms.uniontech.com/testcase-browse-47.html"
    # print(rx.open_url(url))

    rx = RequestX()
    url = "https://www.baidu.com"
    print(rx.open_url(url))
