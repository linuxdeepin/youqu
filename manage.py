#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
# pylint: disable=wrong-import-position
import os
import sys
import traceback
from argparse import ArgumentParser

from setting.globalconfig import GlobalConfig
from setting.globalconfig import SystemPath

os.environ["DISPLAY"] = ":0"
os.environ["PIPENV_VERBOSITY"] = "-1"
os.environ["XAUTHORITY"] = f"{GlobalConfig.HOME}/.Xauthority"

for i in SystemPath:
    if i.value in sys.path:
        continue
    sys.path.append(i.value)

from funnylog import logger
from funnylog.conf import setting as log_setting

log_setting.LOG_FILE_PATH = GlobalConfig.REPORT_PATH


class Manage:
    __author__ = "mikigo<huangmingqiang@uniontech.com>"

    def __init__(
        self,
        app=None,
        keywords=None,
        tags=None,
        rerun=None,
        record_failed_case=None,
        clean=None,
        report_formats=None,
        max_fail=None,
        log_level=None,
        timeout=None,
        resolution=None,
        debug=None,
        noskip=None,
        ifixed=None,
        send_pms=None,
        task_id=None,
        trigger=None,
        case_file=None,
        branch=None,
        deb_path=None,
        pms_user=None,
        pms_password=None,
        suite_id=None,
        pms_info_file=None,
        top=None,
        lastfailed=None,
        duringfail=None,
        repeat=None,
        project_name=None,
        build_location=None,
        line=None,
        client=None,
        send_code=None,
        build_env=None,
        client_password=None,
        parallel=None,
        autostart=None,
        pyid2csv=None,
        export_csv_file=None,
        pms2csv=None,
        csv2pms=None,
        csv_name=None,
        pms_link_csv=None,
        send2task=None,
        url=None,
        startdate=None,
        enddate=None,
        git_user=None,
        git_password=None,
        depth=None,
        slaves=None,
    ):
        self.default_app = app
        self.default_keywords = keywords
        self.default_tags = tags
        self.default_rerun = rerun
        self.default_record_failed_case = record_failed_case
        self.default_clean = clean
        self.default_report_formats = report_formats
        self.default_max_fail = max_fail
        self.default_log_level = log_level
        self.default_timeout = timeout
        self.default_resolution = resolution
        self.default_debug = debug
        self.default_noskip = noskip
        self.default_ifixed = ifixed
        self.default_send_pms = send_pms
        self.default_task_id = task_id
        self.default_trigger = trigger
        self.default_case_file = case_file
        self.default_branch = branch
        self.default_deb_path = deb_path
        self.default_pms_user = pms_user
        self.default_pms_password = pms_password
        self.default_suite_id = suite_id
        self.default_pms_info_file = pms_info_file
        self.default_top = top
        self.default_lastfailed = lastfailed
        self.default_duringfail = duringfail
        self.default_repeat = repeat
        self.default_project_name = project_name
        self.default_build_location = build_location
        self.default_line = line
        self.default_client = client
        self.default_send_code = send_code
        self.default_build_env = build_env
        self.default_client_password = client_password
        self.default_parallel = parallel
        self.default_autostart = autostart
        self.default_pyid2csv = pyid2csv
        self.default_export_csv_file = export_csv_file
        self.default_pms2csv = pms2csv
        self.default_csv2pms = csv2pms
        self.default_csv_name = csv_name
        self.default_pms_link_csv = pms_link_csv
        self.default_send2task = send2task
        self.default_url = url
        self.default_startdate = startdate
        self.default_enddate = enddate
        self.default_git_user = git_user
        self.default_git_password = git_password
        self.default_depth = depth
        self.default_slaves = slaves
        from src.plugins.mng import trim

        trim()
        logger(GlobalConfig.LOG_LEVEL)

        self.cmd_args = sys.argv[1:]
        parser = ArgumentParser(epilog=self.__author__)
        subparsers = parser.add_subparsers(help="子命令")
        from src.plugins.mng import SubCmd

        sub_parser_remote = subparsers.add_parser(SubCmd.remote.value)
        sub_parser_run = subparsers.add_parser(SubCmd.run.value)
        sub_parser_playbook = subparsers.add_parser(SubCmd.playbook.value)
        sub_parser_pms = subparsers.add_parser(SubCmd.pmsctl.value)
        sub_parser_csv = subparsers.add_parser(SubCmd.csvctl.value)
        sub_parser_git = subparsers.add_parser(SubCmd.git.value)

        from src.plugins.mng import help_tip

        if not self.cmd_args:
            print(help_tip())
            sys.exit(1)

        if self.cmd_args[0] == SubCmd.remote.value:
            from src.rtk._cargo import remote_runner
            from src.rtk.remote_runner import RemoteRunner

            remote_kwargs = remote_runner(self, parser, sub_parser_remote)
            RemoteRunner(**remote_kwargs).remote_run()

        elif self.cmd_args[0] == SubCmd.run.value:
            from src.rtk._cargo import local_runner
            from src.rtk.local_runner import LocalRunner

            _local_kwargs, _ = local_runner(self, parser, sub_parser_run)
            LocalRunner(**_local_kwargs).local_run()
        elif self.cmd_args[0] == SubCmd.playbook.value:
            from src.rtk._cargo import playbook_control

            playbook_control(parser, sub_parser_playbook)

        elif self.cmd_args[0] == SubCmd.pmsctl.value:
            from src.pms._cargo import pms_control

            pms_control(self, parser, sub_parser_pms)

        elif self.cmd_args[0] == SubCmd.csvctl.value:
            from src.rtk._cargo import csv_control

            csv_control(self, parser, sub_parser_csv)

        elif self.cmd_args[0] == SubCmd.startapp.value:
            start_config_log = f"{SubCmd.startapp.value} 后面直接加工程名称"
            try:
                if self.cmd_args[1] in ("-h", "--help"):
                    print(start_config_log)
                    sys.exit(0)
                from src.plugins.mng import start_app

                start_app(self.cmd_args[1])
            except IndexError:
                logger.error(f"参数异常: {start_config_log}")

        elif self.cmd_args[0] == SubCmd.git.value:
            from src.git._cargo import git_control

            git_control(self, parser, sub_parser_git)

        elif self.cmd_args[0] in ["-h", "--help"]:
            print(help_tip())

        else:
            print(f"参数异常 \033[0;31m{self.cmd_args}\033[0m!\n{help_tip()}")


if __name__ == "__main__":
    try:
        Manage()
    except Exception as exc:
        traceback.print_exception(*sys.exc_info())
