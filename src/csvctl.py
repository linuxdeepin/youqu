#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
import os
import re
from collections import Counter

from setting.globalconfig import GlobalConfig, FixedCsvTitle
from src.rtk._base import transform_app_name


class CsvControl:

    def __init__(self, app_name=None):
        self.walk_dir = (
            f"{GlobalConfig.APPS_PATH}/{transform_app_name(app_name)}"
            if app_name
            else GlobalConfig.APPS_PATH
        )
        self.csv_path_dict, self.py_path_dict = self.scan_csv_and_py()

    def scan_csv_and_py(self):
        csv_path_dict = {}
        py_path_dict = {}
        for root, _, files in os.walk(self.walk_dir):
            py_files = []
            for file in files:
                if file.endswith(".csv") and file != "case_list.csv":
                    csv_path_dict[os.path.splitext(file)[0]] = f"{root}/{file}"
                if file.startswith("test_") and file.endswith(".py"):
                    case_name = []
                    _case_name = re.findall(r"test_(.*?)_(\d+)_\d+.py|test_(.*?)_(\d+).py", file)
                    if _case_name:
                        _case_name = _case_name[0]
                        if isinstance(_case_name, tuple):
                            for i in _case_name:
                                if i:
                                    case_name.append(i)

                    if py_path_dict.get(case_name[0]):
                        tmp_py_list = py_path_dict.get(case_name[0])
                        tmp_py_list.append([f"{root}/{file}", root, case_name[-1]])
                        py_path_dict[case_name[0]] = tmp_py_list
                    else:
                        py_files.append([f"{root}/{file}", root, case_name[-1]])
                        py_path_dict[case_name[0]] = py_files

        for i in py_path_dict:
            py_path_dict[i] = sorted(py_path_dict[i], key=lambda x: int(x[-1]))
        return csv_path_dict, py_path_dict

    def delete_mark_in_csv_if_not_exists_py(self):
        res = self.scan_csv_and_py()
        if res is None:
            return
        csv_path_dict, py_path_dict = res
        flag = False
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
                            raise ValueError(
                                f"文件：{csv_path} 里面似乎格式有点问题,出现了一个报错：{e}"
                            )
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
                        flag = True
        if flag:
            print("The corresponding script ID no longer exists in the CSV file after deletion")

    def async_mark_to_csv(self):
        """async_mark_to_csv"""
        self.csv_path_dict, self.py_path_dict = self.scan_csv_and_py()
        for case_name in self.py_path_dict:
            py_paths = self.py_path_dict.get(case_name)
            py_count = Counter([i[1] for i in py_paths])
            is_one = len(py_paths) == 1 or len(py_count) == 1
            for py_path, py_dirpath, case_id in py_paths:
                if not self.csv_path_dict or not self.csv_path_dict.get(case_name):
                    _dir_name = os.path.dirname(os.path.abspath(py_path))
                    if is_one:
                        if str(_dir_name).endswith("case"):
                            dir_name = self.walk_dir
                        else:
                            dir_name = os.path.dirname(_dir_name.replace("/case/", "/tag/"))
                    else:
                        dir_name = self.walk_dir
                    if not os.path.exists(dir_name):
                        os.makedirs(dir_name)

                    csv_path = f"{dir_name}/{case_name}.csv"
                    with open(csv_path, "w+", encoding="utf-8") as f:
                        f.write(",".join([i.value for i in FixedCsvTitle]) + "\n")

                    self.csv_path_dict, self.py_path_dict = self.scan_csv_and_py()

                csv_path = self.csv_path_dict.get(case_name)
                with open(csv_path, "r", encoding="utf-8") as f:
                    csv_txt_list = f.readlines()
                    try:
                        csv_head = csv_txt_list[0]
                        comma_num = csv_head.count(",")
                    except IndexError:
                        with open(csv_path, "w+", encoding="utf-8") as f:
                            f.write(",".join([i.value for i in FixedCsvTitle]) + "\n")
                        comma_num = len(FixedCsvTitle) - 1
                csv_taglines = [txt.strip().split(",") for txt in csv_txt_list[1:]]
                if not csv_taglines:
                    with open(csv_path, "a+", encoding="utf-8") as f:
                        f.write(f"{case_id}{comma_num * ','}" + "\n")
                else:
                    for i in csv_taglines:
                        if i[0] == case_id or int(i[0]) == int(case_id):
                            break
                    else:
                        with open(csv_path, "a+", encoding="utf-8") as f:
                            f.write(f"{case_id}{comma_num * ','}" + "\n")
        print("完成自动化用例脚本同步到CSV文件。")


if __name__ == "__main__":
    CsvControl().delete_mark_in_csv_if_not_exists_py()
    CsvControl().async_mark_to_csv()
