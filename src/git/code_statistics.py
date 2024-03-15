#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import os
import json
from copy import deepcopy
from difflib import unified_diff
from datetime import datetime

from setting import conf
from src.rtk._base import transform_app_name
from src.git.commit import Commit


class CodeStatistics(Commit):
    __author__ = "mikigo<huangmingqiang@uniontech.com>"

    def __init__(
        self,
        app_name: str,
        branch: str,
        startdate: str = None,
        enddate: str = None,
        **kwargs,
    ):
        self.app_name = transform_app_name(app_name or conf.APP_NAME)
        self.repo_path = f"{conf.APPS_PATH}/{self.app_name}"
        self.branch = branch or conf.BRANCH
        self.startdate = startdate or conf.START_DATE

        if startdate:
            super().__init__(app_name, branch=branch, startdate=startdate, enddate=enddate)
        self.ignore_txt = ["from", "import"]

        for i in range(100):
            self.ignore_txt.append(" " * i + "#")

    def get_git_files(self, end_commit_id, max_width=10000):
        git_files = []
        _files = os.popen(f"cd {self.repo_path};git show --stat={max_width} {end_commit_id}").read()
        files = _files.split("\n")
        for file_info in files:
            if "| " not in file_info:
                continue
            file_path = file_info.split("| ")[0].replace(" ", "")
            if file_path.endswith(".py") and not file_path.split("/")[-1].startswith("__"):
                git_files.append(file_path)
        return git_files

    def compare_files(self, start_commit_id, end_commit_id, author, git_dt: datetime):
        _fix_debug = []
        _new_debug = []
        new_test_case_num = 0
        del_test_case_num = 0
        fix_test_case_num = 0
        new_method_num = 0
        del_method_num = 0
        fix_method_num = 0
        git_files = self.get_git_files(end_commit_id=end_commit_id)
        for filepath in git_files:
            filename = filepath.split("/")[-1]
            print("filepath:", filepath, "\n")
            start_code = (
                os.popen(f"cd {self.repo_path}/;git show {start_commit_id}:{filepath}")
                .read()
                .splitlines()
                or ""
            )
            end_code = (
                os.popen(f"cd {self.repo_path}/;git show {end_commit_id}:{filepath}")
                .read()
                .splitlines()
                or ""
            )
            dif_gen = unified_diff(start_code, end_code, fromfile="start", tofile="end")
            dif_txt = "\n".join(dif_gen)
            print("=" * 100)
            # case
            if filename.startswith("test_"):
                _contents = dif_txt.splitlines()
                contents = _contents[6:]
                added = reduced = unchanged = False
                for line in contents:
                    if line.startswith("+"):
                        added = True
                    elif line.startswith("-"):
                        reduced = True
                    else:
                        if line.startswith(tuple(self.ignore_txt)):
                            continue
                        unchanged = True

                if all(
                    [
                        added is True,
                        reduced is False,
                        unchanged is False,
                    ]
                ):
                    new_test_case_num += 1
                if all(
                    [
                        added is False,
                        reduced is True,
                        unchanged is False,
                    ]
                ):
                    del_test_case_num += 1
                if all(
                    [
                        any(
                            [
                                added is True,
                                reduced is True,
                            ]
                        ),
                        unchanged is True,
                    ]
                ):
                    fix_test_case_num += 1
            # method
            else:
                print(dif_txt)
                methods = []
                method_info = {}
                for line in dif_txt.splitlines():
                    if line.startswith(("---", "+++", "@@", "@")):
                        continue
                    if "def " in line:
                        if method_info:
                            methods.append(method_info)
                            method_info = {}
                        method_info["name"] = line
                    else:
                        if method_info.get("method_content"):
                            method_info["method_content"].append(line)
                        else:
                            method_info["method_content"] = [line]
                methods.append(method_info)
                for method in methods:
                    method_name = method.get("name")
                    method_content = method.get("method_content")

                    if method_name is None:
                        if method_content:
                            for content in method_content:
                                if content.startswith(("-", "+")):
                                    if content[1:].startswith(tuple(self.ignore_txt)):
                                        continue
                                    _fix_debug.append(method)
                                    fix_method_num += 1
                                    break

                    # 正常出现的方法
                    # 方法名称是+开头，直接视为新增方法
                    elif method_name.startswith("+"):
                        _new_debug.append(method)
                        new_method_num += 1
                    # 方法名称是-开头，直接视为删除方法
                    elif method_name.startswith("-"):
                        del_method_num += 1
                    else:
                        if method_content:
                            for content in method_content:
                                if content.startswith(("-", "+")):
                                    _fix_debug.append(method)
                                    fix_method_num += 1
                                    break

        res = {
            "start_commit_id": start_commit_id,
            "end_commit_id": end_commit_id,
            "author": author,
            "git_dt": git_dt.strftime("%Y-%m-%d"),
            "branch": self.branch,
            "新增用例": new_test_case_num,
            "删除用例": del_test_case_num,
            "修改用例": fix_test_case_num,
            "新增方法": new_method_num,
            "删除方法": del_method_num,
            "修改方法": fix_method_num,
        }
        return res

    def write_result(self, res, detail=False):
        if not os.path.exists(conf.REPORT_PATH):
            os.makedirs(conf.REPORT_PATH)
        result_file = os.path.join(
            conf.REPORT_PATH,
            f"{self.app_name}_git_compare_result{f'_detail' if detail else ''}.json",
        )
        with open(result_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(res, ensure_ascii=False, indent=4, default=None))

        with open(result_file, "r", encoding="utf-8") as f:
            print(f.read())
        print(f"数据结果报告：{result_file}")

    def codex(self):
        results = None
        results_detail = []
        if self.startdate:
            commit_id_pairs = self.commit_id()
            results = {}
            for i, (_start_commit_id, _end_commit_id, _author, git_dt) in enumerate(
                commit_id_pairs
            ):
                _res = self.compare_files(_start_commit_id, _end_commit_id, _author, git_dt)
                res = deepcopy(_res)
                results_detail.append(_res)
                author = res["author"]
                new_test_case_num = res["新增用例"]
                del_test_case_num = res["删除用例"]
                fix_test_case_num = res["修改用例"]
                new_method_num = res["新增方法"]
                del_method_num = res["删除方法"]
                fix_method_num = res["修改方法"]
                commit_new = res["end_commit_id"]
                if results.get(author) is None:
                    results[author] = res
                else:
                    results[author]["新增用例"] += new_test_case_num
                    results[author]["删除用例"] += del_test_case_num
                    results[author]["修改用例"] += fix_test_case_num
                    results[author]["新增方法"] += new_method_num
                    results[author]["删除方法"] += del_method_num
                    results[author]["修改方法"] += fix_method_num
                    results[author]["end_commit_id"] = commit_new

        if results is None:
            raise ValueError()
        self.write_result(results)
        if results_detail:
            self.write_result(results_detail, detail=True)


if __name__ == "__main__":
    app_name = "apps/autotest_deepin_downloader"
    CodeStatistics(
        app_name=app_name,
        branch="master",
        startdate="2024-02-25",
        # enddate="2024-02-23",
    ).codex()
