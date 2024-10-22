#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
import json
import os
from os import makedirs
from os.path import exists
from re import findall, sub

from setting.globalconfig import GlobalConfig
from src import logger
from src.requestx import RequestX

MAX_CASE_NUMBER = 10000
runs_id_cmd_log = lambda x: sub(r"'run_case_id': '\d+', ", "", str(x))


class _Base:
    __author__ = "huangmingqiang@uniontech.com"

    def __init__(self, user=None, password=None):
        login_url = "https://pms.uniontech.com/user-login-Lw==.html"
        headers = {"content-type": "application/x-www-form-urlencoded; charset=UTF-8"}
        data = {
            "account": user if user else GlobalConfig.PMS_USER,
            "password": password if password else GlobalConfig.PMS_PASSWORD,
            "passwordStrength": "1",
            "referer": "/zentao/",
            "verifyRand": "370729017",
            "keepLogin": "0",
        }
        # pylint: disable=invalid-name
        self.rx = RequestX(login_url=login_url, headers=headers, data=data)


def write_case_result(item, report):
    """写用例执行的结果"""
    case_result_tpl = {
        "at_case_id": None,
        "case_id": None,
        "from_case_id": None,
        "task_id": None,
        "run_case_id": None,
        "result": None,
    }
    try:
        at_case_id = findall(r"test_.*?_(\d+)", item.name)[0]
    except IndexError:
        return
    taskid = item.config.option.task_id
    suiteid = item.config.option.suite_id
    caseid = None
    run_case_id = None
    from_case_id = None
    for mark in item.own_markers:
        if mark.args and isinstance(mark.args[0], str) and mark.args[0].strip("*") == "PMS用例ID":
            caseid = mark.name
        elif mark.args == ("run_case_id",):
            run_case_id = mark.name
        elif mark.args == ("from_case_id",):
            from_case_id = mark.name

    if None in (caseid, run_case_id):
        logger.error(f"{item.name},case_id 或 run_case_id 没获取到")

    case_result_tpl["run_case_id"] = run_case_id
    case_result_tpl["case_id"] = caseid
    case_result_tpl["from_case_id"] = from_case_id
    case_result_tpl["task_id"] = taskid or suiteid
    case_result_tpl["at_case_id"] = at_case_id
    case_result_tpl["item"] = item.name
    case_result_tpl["result"] = "pass" if report.outcome == "passed" else "fail"
    case_res_path = item.session.case_res_path
    if not exists(case_res_path):
        makedirs(case_res_path)

    json_file_name = f"{os.path.splitext(item.fspath.basename)[0]}.json"
    abs_json_file_path = f"{case_res_path}/{json_file_name}"
    if exists(abs_json_file_path):
        with open(abs_json_file_path, "r", encoding="utf-8") as _f:
            case_res_from_json = json.load(_f)

        if hasattr(item, "execution_count")  and item.execution_count >= 2:
            if (
                case_res_from_json.get("result") == "fail"
                and case_result_tpl["result"] == "pass"
                and case_res_from_json.get("item") == case_result_tpl["item"]
            ):
                case_result_tpl["result"] = "cover-pass"
                with open(abs_json_file_path, "w+", encoding="utf-8") as _f:
                    _f.write(json.dumps(case_result_tpl, indent=2, ensure_ascii=False))
        else:
            if (
                case_res_from_json.get("result") in ("pass", "cover-pass")
                and case_result_tpl["result"] == "fail"
            ):
                with open(abs_json_file_path, "w+", encoding="utf-8") as _f:
                    _f.write(json.dumps(case_result_tpl, indent=2, ensure_ascii=False))
    else:
        with open(abs_json_file_path, "w+", encoding="utf-8") as _f:
            _f.write(json.dumps(case_result_tpl, indent=2, ensure_ascii=False))
