#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import os
import json

from setting import conf
from difflib import unified_diff

from src.rtk._base import transform_app_name


class CodeStatistics:
    __author__ = "mikigo<huangmingqiang@uniontech.com>"

    def __init__(self, app_name: str, commit_new: str, commit_old: str, **kwargs):
        self.app_name = transform_app_name(app_name)
        self.repo_path = f"{conf.APPS_PATH}/{self.app_name}"
        self.commit_new = commit_new
        self.commit_old = commit_old
        self.ignore_txt = ["from", "import", ""]

        for i in range(100):
            self.ignore_txt.append(" " * i + "#")

        self._debug = []

    def get_git_files(self):
        diffs = os.popen(f"cd {self.repo_path};git diff {self.commit_old} {self.commit_new}").read().split("\n")
        git_files = []
        file_info = {}
        for diff in diffs:
            if diff.startswith("diff --git "):
                if file_info:
                    git_files.append(file_info)
                    file_info = {}
                file_info["file"] = diff
            else:
                if file_info.get("content"):
                    file_info["content"].append(diff)
                else:
                    file_info["content"] = [diff]
        git_files.append(file_info)
        return git_files

    def compare_files(self):
        new_test_case_num = 0
        del_test_case_num = 0
        fix_test_case_num = 0
        new_method_num = 0
        del_method_num = 0
        fix_method_num = 0
        git_files = self.get_git_files()
        for git_file in git_files:
            filepath = git_file.get("file").split(" ")[-1].strip('b/')
            filename = filepath.split("/")[-1]

            if not filename.endswith(".py"):
                print("===== ignoring:", filepath, "\n")
                continue

            print("filepath:", filepath, "\n")
            old_code = os.popen(f"cd {self.repo_path}/;git show {self.commit_old}:{filepath}").read().splitlines() or ""
            new_code = os.popen(f"cd {self.repo_path}/;git show {self.commit_new}:{filepath}").read().splitlines() or ""
            dif_gen = unified_diff(old_code, new_code)
            print("=" * 100)
            # case
            if filename.startswith("test_"):
                contents = git_file.get("content")
                for content in contents:
                    if content.startswith("--- /dev/null"):
                        new_test_case_num += 1
                        break
                    elif content.startswith("+++ /dev/null"):
                        del_test_case_num += 1
                        break
                else:
                    fix_test_case_num += 1
            # method
            else:
                dif_txt = "\n".join(dif_gen)
                print(dif_txt)
                methods = []
                method_info = {}
                for line in dif_txt.splitlines():
                    if line.startswith(
                            ("---", "+++", "@@", "@")
                    ):
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
                                    self._debug.append(method)
                                    fix_method_num += 1
                                    break

                    # 正常出现的方法
                    # 方法名称是+开头，直接视为新增方法
                    elif method_name.startswith("+"):
                        new_method_num += 1
                    # 方法名称是-开头，直接视为删除方法
                    elif method_name.startswith("-"):
                        del_method_num += 1
                    else:
                        if method_content:
                            for content in method_content:
                                if content.startswith(("-", "+")):
                                    self._debug.append(method)
                                    fix_method_num += 1
                                    break

        res = {
            "新增用例": new_test_case_num,
            "删除用例": del_test_case_num,
            "修改用例": fix_test_case_num,
            "新增方法": new_method_num,
            "删除方法": del_method_num,
            "修改方法": fix_method_num,
        }
        return res

    def write_result(self):
        res = self.compare_files()
        with open(os.path.join(conf.REPORT_PATH, f"{self.app_name}_git_compare_result.json"), "w", encoding="utf-8") as f:
            f.write(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    repo = '/home/mikigo/github/deepin-autotest-framework/apps/autotest_deepin_downloader'
    commit_n = '059632e9e2dfc7fe580abefe3c51f15d8672d213'
    commit_o = 'c30572e113a2e90cf340426a8c16c44b7605bfd7'
    CodeStatistics(repo, commit_n, commit_o).write_result()
