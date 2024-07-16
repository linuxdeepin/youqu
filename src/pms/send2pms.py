#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
# pylint: disable=C0301,C0116,W0613,W1514,C0103,C0103
import json
import os
import re
from os.path import exists
import socket
from time import sleep
from urllib.parse import urlencode
from urllib.error import HTTPError

from setting.globalconfig import GlobalConfig
from src import logger
from src.pms._base import _Base
from src.pms._base import runs_id_cmd_log


class Send2Pms(_Base):
    """发送数据到pms"""

    __author__ = "huangmingqiang@uniontech.com"

    def post_to_pms(self, run_case_id=None, case_id=None, result=None, **kwargs):
        base_url = "https://pms.uniontech.com/testtask-runCase"
        # 每次请求时，获取steps_id
        run_case_html_url = f"{base_url}-{run_case_id}.html"
        res = self.rx.open_url(run_case_html_url, timeout=10)
        if res == "":
            # 测试套件回填时地址不一样
            run_case_html_url = f"{base_url}-0-{run_case_id}-1.html"
            res = self.rx.open_url(run_case_html_url, timeout=30)
        steps_id = re.findall(r"name='steps\[(\d+)\]'", res)
        if steps_id and steps_id[0]:
            steps_id = steps_id[0]
        else:
            return 201
        # 构造post数据
        data = {
            f"steps[{steps_id}]": result,
            f"reals[{steps_id}]": "",
            "case": case_id,
            "version": "1",
            f"labels{steps_id}[]": "",
            f"files{steps_id}[]": "",
        }
        bytes_data = urlencode(data).encode("utf-8")
        # post请求接口
        res = self.rx.session.open(fullurl=run_case_html_url, data=bytes_data, timeout=30)
        status_code = res.status
        return status_code

    def send2pms(self, case_res_path, data_send_result_csv):
        """发送数据到PMS"""
        if exists(case_res_path):
            for case_name_json in os.listdir(case_res_path):
                if not case_name_json.endswith(".json"):
                    continue
                with open(f"{case_res_path}/{case_name_json}", "r", encoding="utf-8") as f:
                    data = json.load(f)
                if not exists(data_send_result_csv):
                    with open(data_send_result_csv, "w+", encoding="utf-8") as f:
                        pass
                with open(data_send_result_csv, "r", encoding="utf-8") as f:
                    reqeusted = f.read()
                case_name = case_name_json.split(".")[0]
                case_result = data.get("result")
                if case_name not in reqeusted:
                    self.push(data_send_result_csv, data, case_name, case_result)
                else:
                    if f"{case_name},fail" in reqeusted and case_result == "cover-pass":
                        fix_requested = re.sub(rf"{case_name},fail,request_.*?\n", "", reqeusted)
                        with open(data_send_result_csv, "w+", encoding="utf-8") as f:
                            f.write(fix_requested)
                        self.push(data_send_result_csv, data, case_name, case_result)
                    elif f"{case_name},pass" in reqeusted and case_result == "fail":
                        fix_requested = re.sub(rf"{case_name},pass,request_.*?\n", "", reqeusted)
                        with open(data_send_result_csv, "w+", encoding="utf-8") as f:
                            f.write(fix_requested)
                        self.push(data_send_result_csv, data, case_name, case_result)

    def push(self, data_send_result_csv, data, case_name, case_result):
        if data["result"] == "cover-pass":
            data["result"] = "pass"
        data.pop("item")
        with open(data_send_result_csv, "a+", encoding="utf-8") as f:
            for _ in range(int(GlobalConfig.SEND_PMS_RETRY_NUMBER)):
                try:
                    status_code = self.post_to_pms(**data)
                    if status_code == 200:
                        logger.info(f"{runs_id_cmd_log(data)} 数据回填成功 ✔")
                        if case_result == "cover-pass" and f"{case_name},pass" in f.read():
                            break
                        f.write(f"{case_name},{data['result']},request_ok\n")
                        break
                except (HTTPError, socket.timeout):
                    sleep(1)
            else:
                logger.info(f"{runs_id_cmd_log(data)} 数据回填失败 ✘")
                f.write(f"{case_name},{data['result']},request_fail\n")

    @staticmethod
    def case_res_path(taskid):
        """case_res_path"""
        return f"{GlobalConfig.REPORT_PATH}/pms_{taskid}"

    @classmethod
    def data_send_result_csv(cls, taskid):
        """data_send_result_csv"""
        return f"{cls.case_res_path(taskid)}/send_pms_{taskid}.csv"

    def remote_finish_push(self, res):
        """remote_finish_push"""
        for data in res.values():
            data.pop("item")
            if data["result"] == "cover-pass":
                data["result"] = "pass"
            for _ in range(int(GlobalConfig.SEND_PMS_RETRY_NUMBER)):
                try:
                    status_code = self.post_to_pms(**data)
                    if status_code == 200:
                        logger.info(f"{runs_id_cmd_log(data)} 数据回填成功 ✔")
                        break
                except (HTTPError, socket.timeout):
                    sleep(1)

            else:
                logger.info(f"{runs_id_cmd_log(data)} 数据回填失败 ✘")
