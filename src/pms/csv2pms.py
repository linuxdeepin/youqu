#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
import os
from urllib.parse import urlencode

from setting import conf
from setting.globalconfig import FixedCsvTitle
from src.pms._base import _Base
from src.rtk._base import transform_app_name


class Csv2Pms(_Base):
    __author__ = "mikigo<huangmingqiang@uniontech.com>"

    config_error_log = "请检查您传递的 '命令行参数' 或 setting/globalconfig.ini 里的配置项"

    def __init__(
            self,
            app_name: str = None,
            user: str = None,
            password: str = None,
            csv_name=None
    ):
        super().__init__(user=user, password=password)
        self.username = user
        self.password = user
        self.base_url = "https://pms.uniontech.com"
        self.walk_dir = (
            f"{conf.APPS_PATH}/{transform_app_name(app_name)}"
            if app_name
            else conf.APPS_PATH
        )
        self.csv_name = csv_name or conf.CSV_NAME_TO_PMS

        if not self.csv_name:
            raise EnvironmentError(self.config_error_log)

    def get_csv_info(self):
        csv_path = None
        for root, _, files in os.walk(self.walk_dir):
            for file in files:
                if f"{self.csv_name}.csv" == file:
                    csv_path = f"{root}/{file}"
        if csv_path is None:
            raise FileNotFoundError(self.config_error_log)

        with open(csv_path, "r", encoding="utf-8") as f:
            txt_list = f.readlines()

        csv_heads = txt_list[0].strip().split(",")
        csv_head_index_map = {}
        for index, title in enumerate(csv_heads):
            for i in FixedCsvTitle:
                if i.value == title.strip():
                    csv_head_index_map[i.name] = {
                        "head_name": i.value,
                        "head_index": index,
                    }

        taglines = [txt.strip().split(",") for txt in txt_list[1:]]
        return csv_head_index_map, taglines

    def post_to_pms(self):
        csv_head_index_map, taglines = self.get_csv_info()

        def csv_map(x):
            return csv_head_index_map.get(x).get('head_index')

        for i in taglines:
            case_id = i[csv_map(FixedCsvTitle.case_id.name)]
            edit_url = f"{self.base_url}/testcase-edit-{case_id}.html"
            data = {
                'isAutomation': '是',
            }
            if i[csv_map(FixedCsvTitle.device_type.name)] in ("PPL", "COL"):
                data["deviceType"] = i[csv_map(FixedCsvTitle.device_type.name)]
            if i[csv_map(FixedCsvTitle.case_from.name)] == "是":
                data["caseSource"] = "是"
            if i[csv_map(FixedCsvTitle.online_obj.name)] == "CICD":
                data["lineCD"] = "是"
            bytes_data = urlencode(data).encode("utf-8")
            res = self.rx.session.open(
                fullurl=edit_url,
                data=bytes_data,
                timeout=10
            )
            print(f"{case_id}-{data}—{res.status}")
