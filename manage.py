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

    def __init__(self):
        from src.plugins.mng import trim
        from src.plugins.mng import help_tip
        from src.plugins.mng import SubCmd

        trim()
        logger(GlobalConfig.LOG_LEVEL)

        self.cmd_args = sys.argv[1:]
        if not self.cmd_args:
            print(help_tip())
            sys.exit(1)
        parser = ArgumentParser(epilog=self.__author__)
        subparsers = parser.add_subparsers(help="子命令")

        sub_parser_remote = subparsers.add_parser(SubCmd.remote.value)
        sub_parser_run = subparsers.add_parser(SubCmd.run.value)
        sub_parser_pms = subparsers.add_parser(SubCmd.pmsctl.value)
        sub_parser_csv = subparsers.add_parser(SubCmd.csvctl.value)
        sub_parser_git = subparsers.add_parser(SubCmd.git.value)

        if self.cmd_args[0] == SubCmd.remote.value:
            from src.rtk._cargo import remote_runner
            from src.rtk.remote_runner import RemoteRunner

            remote_kwargs = remote_runner(parser, sub_parser_remote)
            RemoteRunner(**remote_kwargs).remote_run()

        elif self.cmd_args[0] == SubCmd.run.value:
            from src.rtk._cargo import local_runner
            from src.rtk.local_runner import LocalRunner

            _local_kwargs, _ = local_runner(parser, sub_parser_run, self.cmd_args)
            LocalRunner(**_local_kwargs).local_run()

        elif self.cmd_args[0] == SubCmd.pmsctl.value:
            from src.pms._cargo import pms_control

            pms_control(parser, sub_parser_pms)

        elif self.cmd_args[0] == SubCmd.csvctl.value:
            from src.rtk._cargo import csv_control

            csv_control(parser, sub_parser_csv)

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

            git_control(parser, sub_parser_git)

        elif self.cmd_args[0] in ["-h", "--help"]:
            print(help_tip())

        else:
            print(f"参数异常 \033[0;31m{self.cmd_args}\033[0m!\n{help_tip()}")


if __name__ == "__main__":
    try:
        Manage()
    except Exception as exc:
        traceback.print_exception(*sys.exc_info())
