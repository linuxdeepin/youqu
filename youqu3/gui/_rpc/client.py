#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
from xmlrpc.client import ServerProxy


def client(ip, port):
    client = ServerProxy(f"http://{ip}:{port}", allow_none=True)
    return client
