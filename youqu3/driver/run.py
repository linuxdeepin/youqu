#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import os.path
import pathlib
import re
import sys

import pytest

from youqu3 import logger, setting


class Run:
    __author__ = "mikigo <huangmingqiang@uniontech.com>"

    def __init__(
            self,
            path=None,
            keywords=None,
            tags=None,
            setup_plan=None,
            slaves=None,
            txt=None,
            job_start=None,
            job_end=None,
            **kwargs,
    ):
        logger("INFO")

        self.path = path
        self.keywords = keywords
        self.tags = tags
        self.setup_plan = setup_plan
        self.slaves = slaves
        self.txt = txt
        self.job_start = job_start
        self.job_end = job_end

        self.rootdir = pathlib.Path(".").absolute()
        self.report_path = self.rootdir / "report"
        self.html_report_path = self.report_path / "html"
        self.allure_data_path = self.html_report_path / "_data"
        self.allure_html_path = self.html_report_path / "html"
        self.json_report_path = self.report_path / "json"

        from funnylog2.config import config as funnylog2_config

        funnylog2_config.LOG_FILE_PATH = self.report_path

    @staticmethod
    def makedirs(dirs):
        pathlib.Path(dirs).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def set_recursion_limit(strings):
        len_tags = len(re.split("or |and |not ", strings))
        if len_tags >= 999:
            sys.setrecursionlimit(len_tags + 100)

    def read_tags_txt(self):
        youqu_tags_file = os.path.join(self.rootdir, "youqu-tags.txt")
        if os.path.exists(youqu_tags_file):
            with open(youqu_tags_file, "r", encoding="utf-8") as f:
                tags_txt = f.readlines()[0]
                return tags_txt
        return None

    def read_keywords_txt(self):
        youqu_keywords_file = os.path.join(self.rootdir, "youqu-keywords.txt")
        if os.path.exists(youqu_keywords_file):
            with open(youqu_keywords_file, "r", encoding="utf-8") as f:
                keywords_txt = f.readlines()[0]
                return keywords_txt
        return None

    def generate_cmd(self):
        cmd = ["pytest"]

        if self.path:
            cmd.append(self.path)

        keywords_txt = self.read_keywords_txt()
        if self.keywords:
            self.set_recursion_limit(self.keywords)
            cmd.extend(["-k", f"'{self.keywords}'"])
        elif self.txt and keywords_txt is not None:
            self.set_recursion_limit(keywords_txt)
            cmd.extend(["-k", f"'{keywords_txt}'"])

        tags_txt = self.read_tags_txt()
        if self.tags:
            self.set_recursion_limit(self.tags)
            cmd.extend(["-m", f"'{self.tags}'"])
        elif self.txt and tags_txt is not None:
            self.set_recursion_limit(tags_txt)
            cmd.extend(["-m", f"'{tags_txt}'"])

        if self.slaves:
            cmd.extend(["--slaves", f"'{self.slaves}'"])

        if self.setup_plan:
            cmd.append("--setup-plan")
        else:
            cmd.extend([
                "--json-report",
                "--json-report-indent=2",
                "--json-report-omit",
                "collectors",
                "log",
                "keywords",
                f"--json-report-file={self.json_report_path / f'report_{setting.TIME_STRING}.json'}",
                f"--alluredir={self.allure_data_path}",
                "--clean-alluredir",
                "-s",
                "--no-header",
            ])

        cmd.extend([
            f"--maxfail={setting.MAX_FAIL}",
            f"--reruns={setting.RERUNS}",
            f"--timeout={setting.TIMEOUT}",
        ])

        return cmd

    def job_start_driver(self):
        from youqu3.cmd import Cmd
        if self.job_start:
            Cmd.run(self.job_start, timeout=3600)
        for file in os.listdir(self.rootdir):
            if file == "job_start.py":
                Cmd.run(f"cd {self.rootdir} && {sys.executable} {file}")

    def job_end_driver(self):
        from youqu3.cmd import Cmd
        if self.job_end:
            Cmd.run(self.job_end, timeout=3600)
        for file in os.listdir(self.rootdir):
            if file == "job_end.py":
                Cmd.run(f"cd {self.rootdir} && {sys.executable} {file}")

    def run(self):
        if not self.setup_plan:
            self.job_start_driver()
        print(" ".join(self.generate_cmd()))
        pytest.main(
            [i.strip("'") for i in self.generate_cmd()[1:]]
        )
        if self.setup_plan:
            return
        os.makedirs(self.allure_html_path, exist_ok=True)
        try:
            from youqu_html import YouQuHtml
            YouQuHtml.gen(str(self.allure_data_path), str(self.allure_html_path), clean=True)
        except ImportError:
            from youqu3.cmd import Cmd
            from youqu_html_rpc import YouQuHtmlRpc
            from youqu_html_rpc.environment import environment
            from youqu_html_rpc.config import config
            config.SERVER_IP = setting.REPORT_SERVER_IP
            if YouQuHtmlRpc.check_connected():
                rsync = 'rsync -av -e "ssh -o StrictHostKeyChecking=no"'
                report_dirname = f"{setting.TIME_STRING}_{setting.HOST_IP}_{self.rootdir.name}"
                report_server_path = f"{setting.REPORT_BASE_PATH}/{report_dirname}"
                report_server_data_path = f"{report_server_path}/data"
                report_server_html_path = f"{report_server_path}/html"
                YouQuHtmlRpc.makedirs(report_server_data_path)
                environment(self.allure_data_path)
                Cmd.expect_run(
                    f"/bin/bash -c '{rsync} {str(self.allure_data_path)}/ {setting.REPORT_SERVER_SSH_USER}@{setting.REPORT_SERVER_IP}:{report_server_data_path}/'",
                    events={'password': f'{setting.REPORT_SERVER_SSH_PASSWORD}\n'},
                    return_code=True
                )
                YouQuHtmlRpc.gen(report_server_data_path, report_server_html_path, report_dirname)
                report_server_url = f"http://{setting.REPORT_SERVER_IP}/{report_dirname}"
                logger.info(f"html_report_url {report_server_url}")
                with open(f"{self.allure_html_path}/{report_dirname}.txt", "w", encoding="utf-8") as f:
                    f.write(report_server_url)

        self.job_end_driver()


if __name__ == "__main__":
    Run().run()
