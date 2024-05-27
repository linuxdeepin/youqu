#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import json
import re
from collections import deque

from src import logger
from src.pms._base import MAX_CASE_NUMBER
from src.pms._base import _Base


class Suite(_Base):
    """获取测试套件关联的用例"""

    __author__ = "huangmingqiang@uniontech.com"

    def get_suite_data(self, suite_id):
        url = f"https://pms.uniontech.com/testsuite-view-{suite_id}-id_desc-1-{MAX_CASE_NUMBER}-1.json"
        res = self.rx.open_url(url, timeout=10)
        try:
            res_dict = json.loads(res)
        except json.decoder.JSONDecodeError:
            logger.error(f"爬取pms数据失败, 请检查模块 id 是否为: {suite_id}")
            return

        cases = json.loads(res_dict.get("data")).get("cases")
        res_data = deque()
        for run_case_id in cases:
            case_id = cases.get(run_case_id).get("id")
            from_case_id = cases.get(run_case_id).get("fromCaseID")
            case_title = cases.get(run_case_id).get("title")
            res_data.append(
                {
                    "case_id": case_id,
                    "from_case_id": from_case_id,
                    "run_case_id": run_case_id,
                    "case_title": case_title,
                }
            )
        return res_data
