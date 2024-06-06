#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import sys
from os.path import dirname
from os.path import basename
from os.path import abspath
from os import environ

sys.path.append(dirname(dirname(dirname(abspath(__file__)))))

from setting import conf

environ["XAUTHORITY"] = f"{conf.HOME}/.Xauthority"
from src.remotectl._base import check_rpc_started as check_rpc_started
from src.remotectl._base import remote_client as remote_client
from src.remotectl._base import remote_server as remote_server

dogtail_port = 4242


@check_rpc_started(basename(__file__))
def remote_dogtail_ctl(user=None, ip=None, password=None, restart_service=False):
    return remote_client(ip=ip, port=dogtail_port)


if __name__ == "__main__":
    from src.dogtail_utils import DogtailUtils

    remote_server(DogtailUtils(), dogtail_port)
