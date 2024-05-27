#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import json
import re
from collections import deque

from src.pms._base import MAX_CASE_NUMBER
from src.pms._base import _Base


class Task(_Base):
    """获取测试套件关联的用例"""

    __author__ = "huangmingqiang@uniontech.com"

    def get_task_data(self, task_id):
        task_json_url = f"https://pms.uniontech.com/testtask-cases-{task_id}-all-0-id_desc-4-{MAX_CASE_NUMBER}-1.json"
        res = self.rx.open_url(task_json_url, timeout=10)
        try:
            res_dict = json.loads(res)
        except json.decoder.JSONDecodeError:
            raise EnvironmentError(
                f"{task_json_url} 未获取到有效数据！\n 请检查你的PMS账号密码是否正确。"
            )
        runs = json.loads(res_dict.get("data")).get("runs")
        runs_ids = deque()
        for run_case_id in runs:
            # 产品库ID
            case_id = runs.get(run_case_id).get("case")
            # 用例库ID
            from_case_id = runs.get(run_case_id).get("fromCaseID")
            case_title = runs.get(run_case_id).get("title")
            runs_ids.append(
                {
                    "case_id": case_id,
                    "from_case_id": from_case_id,
                    "run_case_id": run_case_id,
                    "case_title": case_title,
                }
            )
        return runs_ids
