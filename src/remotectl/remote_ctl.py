#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import os
import sys
import time
from os.path import dirname
from os.path import basename

try:
    import zerorpc
except ImportError:
    os.system("pip3 install zerorpc -i https://pypi.tuna.tsinghua.edu.cn/simple")
    time.sleep(1)
    import zerorpc

sys.path.append(dirname(dirname(dirname(os.path.abspath(__file__)))))
from setting import conf
from src.remotectl.base import check_rpc_started


@check_rpc_started(basename(__file__))
def remote_ctl(user=None, ip=None, password=None, transfer_appname=None):
    r = zerorpc.Client(timeout=50, heartbeat=None)
    r.connect(f"tcp://{ip}:4243")
    return r


if __name__ == '__main__':
    from os import environ

    environ["XAUTHORITY"] = f"/home/{conf.USERNAME}/.Xauthority"
    from src import Src

    server = zerorpc.Server(Src())
    server.bind("tcp://0.0.0.0:4243")
    server.run()
