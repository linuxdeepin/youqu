#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import json
import os
from copy import deepcopy
from datetime import datetime

from setting import conf
from src.depends.colorama import Fore
from src.git.commit import Commit
from src.rtk._base import transform_app_name
from src import logger


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

        self.ignore_txt = ["from", "import", '"""', '    """', "class", "#", "@"]

        for i in range(100):
            self.ignore_txt.append(" " * i + "#")

    def get_git_files(self, commit_id, max_width=10000):
        git_files = []
        _files = os.popen(f"cd {self.repo_path};git show --stat={max_width} {commit_id}").read()
        files = _files.split("\n")
        for file_info in files:
            if "| " not in file_info:
                continue
            file_path = file_info.split("| ")[0].replace(" ", "")
            if file_path.endswith(".py") and not file_path.split("/")[-1].startswith("__"):
                git_files.append(file_path)
        return git_files

    def compare_files(self, commit_id, author, git_dt: datetime):
        _fix_debug = []
        _new_debug = []
        new_test_case_num = 0
        del_test_case_num = 0
        fix_test_case_num = 0
        new_method_num = 0
        del_method_num = 0
        fix_method_num = 0
        new_test_cases = []
        del_test_cases = []
        fix_test_cases = []
        new_mehthods = []
        del_mehthods = []
        fix_mehthods = []
        git_files = self.get_git_files(commit_id=commit_id)
        for filepath in git_files:
            filename = filepath.split("/")[-1]
            dif_texts = os.popen(f"cd {self.repo_path}/;git show {commit_id} -- {filepath}").read()
            logger.info(Fore.GREEN + ("=" * 100) + Fore.RESET)
            logger.info(filepath + "\n" + dif_texts)
            dif_lines = dif_texts.splitlines()
            # case
            if filename.startswith("test_"):
                for line in dif_lines:
                    if line.startswith("--- /dev/null"):
                        new_test_case_num += 1
                        new_test_cases.append(filepath)
                        break
                    elif line.startswith("+++ /dev/null"):
                        del_test_case_num += 1
                        del_test_cases.append(filepath)
                        break
                else:
                    fix_test_case_num += 1
                    fix_test_cases.append(filepath)
            # method
            else:
                methods = []
                method_info = {}
                for line in dif_lines:
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
                                    if any([
                                        content[1:].startswith(tuple(self.ignore_txt)),
                                        content[1:] == "",
                                        content[1:].endswith(('"""', "@staticmethod", "@classmethod"))
                                    ]):
                                        continue
                                    _fix_debug.append(method)
                                    fix_method_num += 1
                                    fix_mehthods.append(f"{filepath}[{method_name}]")
                                    break

                    # 正常出现的方法
                    # 方法名称是+开头，直接视为新增方法
                    elif method_name.startswith("+"):
                        _new_debug.append(method)
                        new_method_num += 1
                        new_mehthods.append(f"{filepath}[{method_name}]")
                    # 方法名称是-开头，直接视为删除方法
                    elif method_name.startswith("-"):
                        del_method_num += 1
                        del_mehthods.append(f"{filepath}[{method_name}]")
                    else:
                        if method_content:
                            for content in method_content:
                                if content.startswith(("-", "+")):
                                    if any([
                                        content[1:] == "",
                                        content[1:].endswith(('"""', "@staticmethod", "@classmethod"))
                                    ]):
                                        continue
                                    _fix_debug.append(method)
                                    fix_method_num += 1
                                    fix_mehthods.append(f"{filepath}[{method_name}]")
                                    break

        res = {
            "commit_id": commit_id,
            "author": author,
            "git_dt": git_dt.strftime("%Y-%m-%d"),
            "branch": self.branch,
            "新增用例": new_test_case_num,
            "删除用例": del_test_case_num,
            "修改用例": fix_test_case_num,
            "新增方法": new_method_num,
            "删除方法": del_method_num,
            "修改方法": fix_method_num,
            "新增用例明细": new_test_cases,
            "删除用例明细": del_test_cases,
            "修复用例明细": fix_test_cases,
            "新增方法明细": new_mehthods,
            "删除方法明细": del_mehthods,
            "修复方法明细": fix_mehthods,
        }
        return res

    def write_result(self, res, detail=False):
        if not os.path.exists(conf.REPORT_PATH):
            os.makedirs(conf.REPORT_PATH)
        result_file = os.path.join(
            conf.REPORT_PATH,
            f"{self.app_name}_git_commit_result{f'_detail' if detail else ''}.json",
        )
        with open(result_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(res, ensure_ascii=False, indent=4, default=None))

        with open(result_file, "r", encoding="utf-8") as f:
            logger.info(f.read())
        logger.info(f"{Fore.GREEN}数据结果{'详细' if detail else '汇总'}报告：{result_file}{Fore.RESET}")

    def codex(self):
        if not self.startdate:
            raise ValueError

        results_detail = []
        commit_id_pairs = self.commit_id()
        results = {}
        for i, (commit_id, _author, git_dt, msg) in enumerate(commit_id_pairs):
            _res = self.compare_files(commit_id, _author, git_dt)
            res = deepcopy(_res)
            _res["msg"] = "\n".join(msg)
            results_detail.append(_res)
            author = res["author"]
            new_test_case_num = res["新增用例"]
            del_test_case_num = res["删除用例"]
            fix_test_case_num = res["修改用例"]
            new_method_num = res["新增方法"]
            del_method_num = res["删除方法"]
            fix_method_num = res["修改方法"]
            commit_id = res["commit_id"]
            _git_dt = res["git_dt"]
            if results.get(author) is None:
                results[author] = res
            else:
                results[author]["新增用例"] += new_test_case_num
                results[author]["删除用例"] += del_test_case_num
                results[author]["修改用例"] += fix_test_case_num
                results[author]["新增方法"] += new_method_num
                results[author]["删除方法"] += del_method_num
                results[author]["修改方法"] += fix_method_num
                results[author]["commit_id"] = commit_id
                results[author]["git_dt_end"] = _git_dt

        if results is None:
            raise ValueError
        logger.info(Fore.GREEN +  ("=" * 100) + Fore.RESET)
        self.write_result(results)
        if results_detail:
            self.write_result(results_detail, detail=True)


if __name__ == "__main__":
    app_name = "apps/autotest_kernel"
    CodeStatistics(
        app_name=app_name,
        branch="at-develop/eagle",
        startdate="2024-01-01",
        # enddate="2024-02-23",
    ).codex()
