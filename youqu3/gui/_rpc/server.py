#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import inspect
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer


class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer): ...


def server(obj, port):
    server = ThreadXMLRPCServer(("0.0.0.0", port), allow_none=True)
    for func_name, _ in inspect.getmembers(obj, predicate=inspect.isfunction):
        if not func_name.startswith("_"):
            server.register_function(getattr(obj, func_name), func_name)
    server.serve_forever()
