#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
# pylint: disable=C0301,C0116,W0613,W1514,C0103,C0103
import json
import os
import re
from urllib.parse import urljoin

from setting import conf
from src.rtk.api_client import ApiClient


class JsonBackfill:
    __author__ = "huangmingqiang@uniontech.com"

    def __init__(self, base_url, username, password, custom_api="api/youqu/yqresult/"):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.custom_api = custom_api
        self.api = ApiClient(
            base_url=self.base_url,
            username=self.username,
            password=self.password,
        )

    def get_remote_json_data(self, json_path):
        json_res = {}
        for file in os.listdir(json_path):
            if file.startswith("detail_report_") and file.endswith(".json"):
                client_ip = re.findall(r"detail_report_(\d+\.\d+\.\d+\.\d+)\.json", file)
                file_path = os.path.join(json_path, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    json_data = json.load(f)
                    if client_ip:
                        json_res[client_ip[0]] = json_data
        return json_res

    def remote_backfill(self, json_path, json_backfill_task_id):
        json_res = self.get_remote_json_data(json_path)
        tpl = {
            "case": "",
            "task": json_backfill_task_id,
            "result": "",
            "is_closed": "",
            "module": "",
            "longrepr": "",
            "pm_ip": "",
            "owner": "",
        }
        for _ip, res in json_res.items():
            for case_py_path, value in res.items():
                _, module, *_, case_py = case_py_path.split("/")
                tpl["case"] = case_py
                case_id = re.findall(r"test_.*?_(\d+)", case_py)
                if case_id:
                    tpl["case"] = case_id[0]
                tpl["module"] = module
                result = value.get("result")
                tpl["result"] = result
                tpl["is_closed"] = False if result == "fail" else True
                tpl["longrepr"] = value.get("longrepr")
                tpl["pm_ip"] = _ip
                res = self.api.post(
                    url=urljoin(self.base_url, self.custom_api),
                    json=tpl
                )
                print(self.custom_api, res)


if __name__ == '__main__':
    JsonBackfill(
        base_url="http://10.7.55.191:8000",
        username="",
        password="",
    ).remote_backfill(f"{conf.REPORT_PATH}/json/0524上午113458_remote/", "d3439082af374a94b95e1d3c0613f513")
