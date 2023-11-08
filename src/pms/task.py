#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114,C0301,C0116,W0707,R0903
import json
import re
from collections import deque

from src.pms._base import _Base
from src.pms._base import _unicode_to_cn
from src.pms._base import MAX_CASE_NUMBER


class Task(_Base):
    """获取测试套件关联的用例"""

    __author__ = "huangmingqiang@uniontech.com"

    def get_task_data(self, task_id):
        task_json_url = f"https://pms.uniontech.com/testtask-cases-{task_id}-all-0-id_desc-4-{MAX_CASE_NUMBER}-1.json"
        res = self.rx.open_url(task_json_url, timeout=10)
        res_str = _unicode_to_cn(res)
        try:
            res_dict = json.loads(res_str)
        except json.decoder.JSONDecodeError:
            raise EnvironmentError(f"{task_json_url} 未获取到有效数据！\n 请检查你的PMS账号密码是否正确。")
        runs = res_dict.get("data").get("runs")
        runs_ids = deque()
        for run_case_id in runs:
            # 产品库ID
            case_id = runs.get(run_case_id).get("case")
            # 用例库ID
            from_case_id = runs.get(run_case_id).get("fromCaseID")
            case_title = runs.get(run_case_id).get("title")
            at_case_id = re.findall(r"\[(\d{3})\]", case_title)
            try:
                at_case_id = at_case_id[0]
            except IndexError:
                at_case_id = "   "
            runs_ids.append(
                {
                    "at_case_id": at_case_id,
                    "case_id": case_id,
                    "from_case_id": from_case_id,
                    "run_case_id": run_case_id,
                    "case_title": case_title,
                }
            )
        return runs_ids
