#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import os
import re
import locale
from datetime import datetime
from datetime import timedelta
from collections import deque

from setting import conf
from src.rtk._base import transform_app_name

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")


class Commit:
    __author__ = "mikigo<huangmingqiang@uniontech.com>"

    def __init__(self, app_name: str, branch: str, startdate: str, enddate: str = None):
        self.app_name = transform_app_name(app_name)
        self.startdate = datetime.strptime(startdate, "%Y-%m-%d")
        self.enddate = (
            self.now_dt
            if enddate == "" or enddate is None
            else datetime.strptime(enddate, "%Y-%m-%d") + timedelta(days=1)
        )
        self.branch = branch
        if self.branch is None:
            raise ValueError("branch 参数必传")

    @property
    def now_dt(self):
        return datetime.strptime(datetime.now().strftime("%Y-%m-%d-%H-%M"), "%Y-%m-%d-%H-%M")

    @property
    def git_logs(self) -> list:
        _git_logs = (
            os.popen(f"cd {conf.APPS_PATH}/{self.app_name} && git log {self.branch}")
            .read()
            .splitlines()
        )
        git_logs = []
        tmp = []
        for line in _git_logs:
            if line.startswith("commit "):
                if tmp:
                    git_logs.append(tmp)
                    tmp = []
                tmp.append(line.split(" ")[1].strip())
            elif line.startswith("Author:"):
                tmp.append(line.split("Author: ")[-1])
            elif line.startswith("Date: "):
                tmp.append(line.split("Date: ")[1].strip())
            else:
                if line.strip() and not line.strip().startswith("Change-Id"):
                    tmp.append(line.strip())
        return git_logs

    def commit_id(self):
        commit_ids = deque()
        for commit_id, author, _time_str, *msg in self.git_logs:
            time_str = " ".join(_time_str.split(" ")[:-1])
            try:
                git_dt = datetime.strptime(time_str, "%a %b %d %H:%M:%S %Y")
            except ValueError:
                continue

            if self.startdate <= git_dt <= self.enddate:
                commit_ids.appendleft([commit_id, author, git_dt, msg])

        if not commit_ids:
            raise ValueError(f"{self.startdate} 到 {self.enddate} 没有获取到有效的 commit id")

        return commit_ids


if __name__ == "__main__":
    Commit(
        app_name="apps/autotest_kernel",
        branch="at-develop/eagle",
        startdate="2024-05-20",
    ).commit_id()
