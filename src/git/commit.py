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
            if enddate is None
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
        git_logs = re.findall(
            r"commit (.*?)\nAuthor: (.*?)\nDate:   (.*?)\n",
            os.popen(f"cd {conf.APPS_PATH}/{self.app_name} && git log {self.branch}").read(),
        )
        return git_logs

    def commit_id(self):
        commit_ids = deque()
        flag = False
        for commit_id, author, _time_str in self.git_logs:
            time_str = " ".join(_time_str.split(" ")[:-1])
            git_dt = datetime.strptime(time_str, "%a %b %d %H:%M:%S %Y")

            if self.startdate <= git_dt <= self.enddate:
                commit_ids.appendleft([commit_id, author, git_dt])
            elif git_dt < self.startdate:
                if flag is False:
                    commit_ids.appendleft([commit_id, None, None])
                    flag = True

        if commit_ids:
            commit_id_pairs = [
                [commit_ids[i][0], commit_ids[i + 1][0], commit_ids[i + 1][1], commit_ids[i + 1][2]] for i in range(len(commit_ids) - 1)
            ]
            return commit_id_pairs

        raise ValueError(f"{self.startdate} 到 {self.enddate} 没有获取到有效的 commit id")


if __name__ == "__main__":
    Commit(
        app_name="apps/autotest_deepin_downloader",
        branch="master",
        startdate="2024-02-27",
    ).commit_id()
