#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
import os
from enum import Enum
from enum import unique
from setting import conf


# pylint: disable=C0103


@unique
class SubCmd(Enum):
    """SubCmd"""
    run = "run"
    remote = "remote"
    pmsctl = "pmsctl"
    startapp = "startapp"
    csvctl = "csvctl"


@unique
class Args(Enum):
    """Args"""
    app_name = "app_name"
    keywords = "keywords"
    tags = "tags"
    reruns = "reruns"
    record_failed_case = "record_failed_case"
    clean = "clean"
    report_formats = "report_formats"
    max_fail = "max_fail"
    log_level = "log_level"
    timeout = "timeout"
    debug = "debug"
    noskip = "noskip"
    ifixed = "ifixed"
    send_pms = "send_pms"
    task_id = "task_id"
    trigger = "trigger"
    resolution = "resolution"
    case_file = "case_file"
    branch = "branch"
    deb_path = "deb_path"
    pms_user = "pms_user"
    pms_password = "pms_password"
    suite_id = "suite_id"
    pms_info_file = "pms_info_file"
    top = "top"
    lastfailed = "lastfailed"
    duringfail = "duringfail"
    repeat = "repeat"
    project_name = "project_name"
    build_location = "build_location"
    line = "line"
    clients = "clients"
    send_code = "send_code"
    build_env = "build_env"
    client_password = "client_password"
    parallel = "parallel"
    autostart = "autostart"
    pyid2csv = "pyid2csv"
    export_csv_file = "export_csv_file"
    pms2csv = "pms2csv"
    pms_link_csv = "pms_link_csv"
    send2task = "send2task"


def  transform_app_name(app_name):
    """转换 app_name"""
    if not app_name:
        return None
    if "-" in app_name:
        raise ValueError(f"{app_name} 中存在 ['-'] 符号")
    if app_name.startswith("apps/"):
        app_name = app_name.replace("apps/", "").strip("/")
    for dir_name in os.listdir(conf.APPS_PATH):
        if dir_name == app_name:
            return app_name
    raise NotADirectoryError(f"{app_name} 目录不存在")
