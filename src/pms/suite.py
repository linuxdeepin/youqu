#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
# pylint: disable=C0301,C0116,R1710,W0201,R0903
import json
import re
from collections import deque

from src  import logger
from src.pms._base import _Base
from src.pms._base import _unicode_to_cn
from src.pms._base import MAX_CASE_NUMBER


class Suite(_Base):
    """获取测试套件关联的用例"""

    __author__ = "huangmingqiang@uniontech.com"

    def get_suite_data(self, suite_id):
        url = f"https://pms.uniontech.com/testsuite-view-{suite_id}-id_desc-1-{MAX_CASE_NUMBER}-1.json"
        self.res = self.rx.open_url(url, timeout=10)
        res_str = _unicode_to_cn(self.res)
        try:
            res_dict = json.loads(res_str)
        except json.decoder.JSONDecodeError:
            logger.error(f"爬取pms数据失败, 请检查模块 id 是否为: {suite_id}")
            return

        cases = res_dict.get("data").get("cases")
        res_data = deque()
        for run_case_id in cases:
            # 产品库ID
            case_id = cases.get(run_case_id).get("id")
            # 用例库ID
            from_case_id = cases.get(run_case_id).get("fromCaseID")
            case_title = cases.get(run_case_id).get("title")
            # 从用例标题中取出自动化用例id [001]
            at_case_id = re.findall(r"\[(\d{3})\]", case_title)
            # 如果id存在，并且之前没有出现过
            try:
                at_case_id = at_case_id[0]
            except IndexError:
                at_case_id = "   "
            res_data.append(
                {
                    "at_case_id": at_case_id,
                    "case_id": case_id,
                    "from_case_id": from_case_id,
                    "run_case_id": run_case_id,
                    "case_title": case_title,
                }
            )

        return res_data
