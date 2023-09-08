#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
import os
import re

from setting.globalconfig import GlobalConfig
from src.rtk._base import transform_app_name


class CsvControl:
    """csv control"""

    def __init__(self, app_name=None):
        self.walk_dir = (
            f"{GlobalConfig.APPS_PATH}/autotest_{transform_app_name(app_name).replace('-', '_')}"
            if app_name
            else GlobalConfig.APPS_PATH
        )
        print(1)

    def scan_csv_and_py(self):
        """scan csv and case py"""
        csv_path_dict = {}
        py_path_dict = {}
        for root, _, files in os.walk(self.walk_dir):
            py_files = []
            for file in files:
                if file.endswith(".csv") and file != "case_list.csv":
                    csv_path_dict[os.path.splitext(file)[0]] = f"{root}/{file}"
                if file.startswith("test_") and file.endswith(".py"):
                    case_name = []
                    _case_name = re.findall(
                        r"test_(.*?)_(\d+)_\d+.py|test_(.*?)_(\d+).py", file
                    )
                    if _case_name:
                        _case_name = _case_name[0]
                        if isinstance(_case_name, tuple):
                            for i in _case_name:
                                if i:
                                    case_name.append(i)
                    py_files.append([f"{root}/{file}", case_name[-1]])
                    py_path_dict[case_name[0]] = py_files
        if not (csv_path_dict and py_path_dict):
            return None
        return csv_path_dict, py_path_dict

    def delete_mark_in_csv_if_not_exists_py(self):
        """delete mark in csv if not exists case py"""
        res = self.scan_csv_and_py()
        if res is None:
            return
        csv_path_dict, py_path_dict = res
        for csv_name in csv_path_dict:
            for case_name in py_path_dict:
                if csv_name == case_name:
                    csv_path = csv_path_dict.get(csv_name)
                    with open(csv_path, "r", encoding="utf-8") as f:
                        csv_txt_list = f.readlines()
                    taglines = [txt.strip().split(",") for txt in csv_txt_list[1:]]
                    new_taglines = []
                    py_case_paths = py_path_dict.get(case_name)
                    for tag in taglines:
                        try:
                            csv_case_id = f"{int(tag[0]):0>3}"
                        except ValueError as e:
                            raise ValueError(f"文件：{csv_path} 里面似乎格式有点问题,出现了一个报错：{e}")
                        for py_case in py_case_paths:
                            py_case_id = py_case[-1]
                            if csv_case_id == py_case_id:
                                new_taglines.append(tag)
                                break
                        else:
                            print(f"{tag} will remove from {csv_path}")
                    if new_taglines != taglines:
                        bak_path = f"{GlobalConfig.REPORT_PATH}/pyid2csv_back"
                        if not os.path.exists(bak_path):
                            os.makedirs(bak_path)
                        os.system(
                            f"cp {csv_path} {bak_path}/{GlobalConfig.TIME_STRING}_{csv_name}.csv"
                        )
                        new_csv_list = [csv_txt_list[0]] + [
                            ",".join(i) + "\n" for i in new_taglines
                        ]
                        with open(csv_path, "w+", encoding="utf-8") as f:
                            f.writelines(new_csv_list)


if __name__ == "__main__":
    CsvControl().delete_mark_in_csv_if_not_exists_py()
