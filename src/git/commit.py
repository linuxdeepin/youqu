#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import os
import re
import locale
from datetime import datetime
from datetime import timedelta

from setting import conf
from src.rtk._base import transform_app_name

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")


class Commit:
    __author__ = "mikigo<huangmingqiang@uniontech.com>"

    def __init__(self, app_name: str, startdate: str, enddate: str = None):
        self.app_name = transform_app_name(app_name)
        self.startdate = datetime.strptime(startdate, "%Y-%m-%d")
        self.enddate = (
            self.now_dt
            if enddate is None
            else datetime.strptime(enddate, "%Y-%m-%d") + timedelta(days=1)
        )

    @property
    def now_dt(self):
        return datetime.strptime(datetime.now().strftime("%Y-%m-%d-%H-%M"), "%Y-%m-%d-%H-%M")

    @property
    def git_logs(self) -> list:
        git_logs = re.findall(
            r"commit (.*?)\nAuthor: (.*?)\nDate:   (.*?)\n",
            os.popen(f"cd {conf.APPS_PATH}/{self.app_name} && git log").read(),
        )
        return git_logs

    def commit_id(self):
        start_commit_id = None
        start_commit_date = None
        end_commit_id = None
        end_commit_date = None
        for commit, author, _time_str in self.git_logs:
            time_str = " ".join(_time_str.split(" ")[:-1])
            git_dt = datetime.strptime(time_str, "%a %b %d %H:%M:%S %Y")

            if self.startdate <= git_dt <= self.enddate:
                if end_commit_id is None:
                    end_commit_id = commit
                    end_commit_date = git_dt
            else:
                if end_commit_id and start_commit_id is None:
                    start_commit_id = commit
                    start_commit_date = git_dt

            if start_commit_id and end_commit_id:
                return end_commit_id, start_commit_id

        raise ValueError(f"{self.startdate} 到 {self.enddate} 没有获取到有效的 commit id")


if __name__ == "__main__":
    Commit(
        app_name="apps/autotest_deepin_downloader", startdate="2024-02-25", enddate="2024-02-26"
    ).commit_id()
