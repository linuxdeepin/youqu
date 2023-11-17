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

os.environ["DISPLAY"] = ":0"

from setting.globalconfig import SystemPath

for i in SystemPath:
    if i.value in sys.path:
        continue
    sys.path.append(i.value)

from setting.globalconfig import GlobalConfig
from src.startapp import StartApp
from src import logger
from src.pms.pms2csv import Pms2Csv
from src.rtk._base import SubCmd
from src.rtk._base import Args
from src.rtk.local_runner import LocalRunner
from src.rtk.remote_runner import RemoteRunner
from src.depends.cfonts import say
from src.pms.send2pms import Send2Pms


# pylint: disable=too-many-instance-attributes,broad-except
class Manage:
    """执行器"""

    __author__ = "mikigo<huangmingqiang@uniontech.com>"

    # pylint: disable=too-many-arguments,too-many-locals,too-many-statements
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

        say(GlobalConfig.PROJECT_NAME)
        version_font = "slick"
        say(GlobalConfig.current_tag, font=version_font, space=False)
        say(f"Code: \033[0;32m{GlobalConfig.GITHUB_URL}\033[0m", font="console", space=False)
        say(f"Docs: \033[0;32m{GlobalConfig.DOCS_URL}\033[0m", font="console", space=False)
        say(f"PyPI: \033[0;32m{GlobalConfig.PyPI_URL}\033[0m", font="console", space=False)
        say("=" * 60, font="console", space=False)
        logger(GlobalConfig.LOG_LEVEL)

        self.cmd_args = sys.argv[1:]
        parser = ArgumentParser(epilog=self.__author__)
        subparsers = parser.add_subparsers(help="子命令")
        sub_parser_remote = subparsers.add_parser(SubCmd.remote.value)
        sub_parser_run = subparsers.add_parser(SubCmd.run.value)
        sub_parser_pms = subparsers.add_parser(SubCmd.pmsctl.value)
        sub_parser_csv = subparsers.add_parser(SubCmd.csvctl.value)

        help_tip = (
            f"\033[0;32mmanage.py\033[0m 支持 \033[0;32m{[i.value for i in SubCmd]}\033[0m 命令, "
            "\n您需要传入一个命令,可以使用 \033[0;32m-h\033[0m或\033[0;32m--help\033[0m 查看每个命令参数的详细使用说明,"
            "\n比如: \033[0;32myouqu manage.py run -h\033[0m \n"
        )
        if not self.cmd_args:
            print(help_tip)
            sys.exit(1)
        if self.cmd_args[0] == SubCmd.remote.value:
            remote_kwargs = self.remote_runner(parser, sub_parser_remote)
            RemoteRunner(**remote_kwargs).remote_run()
        elif self.cmd_args[0] == SubCmd.run.value:
            _local_kwargs, _ = self.local_runner(parser, sub_parser_run)
            LocalRunner(**_local_kwargs).local_run()
        elif self.cmd_args[0] == SubCmd.pmsctl.value:
            self.pms_control(parser, sub_parser_pms)
        elif self.cmd_args[0] == SubCmd.csvctl.value:
            self.csv_control(parser, sub_parser_csv)
        elif self.cmd_args[0] == SubCmd.startapp.value:
            start_config_log = f"{SubCmd.startapp.value} 后面直接加工程名称,工程名称以 'autotest_' 开头"
            try:
                if self.cmd_args[1] in ("-h", "--help"):
                    print(start_config_log)
                    sys.exit(0)
                self.start_app(self.cmd_args[1])
            except IndexError:
                logger.error(f"参数异常: {start_config_log}")
        elif self.cmd_args[0] in ["-h", "--help"]:
            print(help_tip)
        else:
            print(f"参数异常 \033[0;31m{self.cmd_args}\033[0m!\n{help_tip}")

    def remote_runner(self, parser, sub_parser_remote):
        """远程执行"""
        sub_parser_remote.add_argument(
            "-c", "--clients", default="",
            help=(
                "远程机器的user@ip:password,多个机器用'/'连接,"
                "如果password不传入,默认取setting/remote.ini中CLIENT_PASSWORD的值,"
                "比如: uos@10.8.13.xx:1 或 uos@10.8.13.xx"
            )
        )
        sub_parser_remote.add_argument(
            "-s", "--send_code", action='store_const', const=True, default=False,
            help="发送代码到测试机（不含report目录）"
        )
        sub_parser_remote.add_argument(
            "-e", "--build_env", action='store_const', const=True, default=False,
            help="搭建测试环境,如果为yes，不管send_code是否为yes都会发送代码到测试机."
        )
        sub_parser_remote.add_argument(
            "-cp", "--client_password", default="", help="测试机密码（全局）"
        )
        sub_parser_remote.add_argument(
            "-y", "--parallel", default="",
            help=(
                "yes:表示所有测试机并行跑，执行相同的测试用例;"
                "no:表示测试机分布式执行，服务端会根据收集到的测试用例自动分配给各个测试机执行。"
            )
        )
        local_kwargs, args = self.local_runner(parser, sub_parser_remote)
        remote_kwargs = {
            Args.clients.value: args.clients or self.default_client,
            Args.send_code.value: args.send_code or self.default_send_code,
            Args.build_env.value: args.build_env or self.default_build_env,
            Args.client_password.value: args.client_password or self.default_client_password,
            Args.parallel.value: args.parallel or self.default_parallel,
        }
        _remote_kwargs = {
            "remote_kwargs": remote_kwargs,
            "local_kwargs": local_kwargs,
        }
        return _remote_kwargs

    def local_runner(self, parser, sub_parser_run):
        """本地执行"""
        sub_parser_run.add_argument(
            "-a", "--app", default="",
            help="应用名称：apps/autotest_deepin_music 或 autotest_deepin_music"
        )
        sub_parser_run.add_argument(
            "-k", "--keywords", default="", help="用例的关键词,支持and/or/not逻辑组合"
        )
        sub_parser_run.add_argument(
            "-t", "--tags", default="", help="用例的标签,支持and/or/not逻辑组合"
        )
        sub_parser_run.add_argument(
            "--rerun", default="", help="失败重跑次数"
        )
        sub_parser_run.add_argument(
            "--record_failed_case", default="", help="失败录屏从第几次失败开始录制视频"
        )
        sub_parser_run.add_argument(
            "--clean", choices=["yes", ""], default="",
            help="清理环境"
        )
        sub_parser_run.add_argument(
            "--report_formats", default="", help="测试报告格式"
        )
        sub_parser_run.add_argument(
            "--max_fail", default="", help="最大失败率"
        )
        sub_parser_run.add_argument(
            "--log_level", default="", help="日志输出级别"
        )
        sub_parser_run.add_argument(
            "--timeout", default="", help="单条用例超时时间"
        )
        sub_parser_run.add_argument(
            "--resolution", default="", help="检查分辨率"
        )
        sub_parser_run.add_argument(
            "--debug", default="", help="调试模式"
        )
        sub_parser_run.add_argument(
            "--noskip", choices=["yes", ""], default="",
            help="csv文件里面标记了skip跳过的用例不生效"
        )
        sub_parser_run.add_argument(
            "--ifixed", choices=["yes", ""], default="",
            help="fixed不生效，仅通过skip跳过用例"
        )
        sub_parser_run.add_argument(
            "--send_pms", choices=["", "async", "finish"], default="",
            help="数据回填"
        )
        sub_parser_run.add_argument(
            "--task_id", default="", help="测试单ID"
        )
        sub_parser_run.add_argument(
            "--trigger", choices=["", "auto", "hand"], default="",
            help="触发者"
        )
        sub_parser_run.add_argument(
            "-f", "--case_file", default="", help="根据文件执行用例"
        )
        sub_parser_run.add_argument(
            "--deb_path", default="", help="需要安装deb包的本地路径"
        )
        sub_parser_run.add_argument(
            "-u", "--pms_user", default="", help="pms 用户名"
        )
        sub_parser_run.add_argument(
            "-p", "--pms_password", default="", help="pms 密码"
        )
        sub_parser_run.add_argument(
            "--suite_id", default="", help="pms 测试套ID"
        )
        sub_parser_run.add_argument(
            "--pms_info_file", default="", help="pms 信息文件"
        )
        sub_parser_run.add_argument(
            "--top", default="", help="过程中记录top命令中的值"
        )
        sub_parser_run.add_argument(
            "--lastfailed", action='store_const', const=True, default=False,
            help="仅执行上次失败用例"
        )
        sub_parser_run.add_argument(
            "--duringfail", action='store_const', const=True, default=False,
            help="测试过程中立即显示报错"
        )
        sub_parser_run.add_argument(
            "--repeat", default="", help="指定用例执行次数"
        )
        sub_parser_run.add_argument(
            "--project_name", default="", help="工程名称（写入json文件）"
        )
        sub_parser_run.add_argument(
            "--build_location", default="", help="构建地区（写入json文件）"
        )
        sub_parser_run.add_argument(
            "--line", default="", help="执行的业务线（写入json文件）"
        )
        sub_parser_run.add_argument(
            "--autostart", default="", help="重启类场景开启letmego执行方案"
        )
        args = parser.parse_args()
        local_kwargs = {
            Args.app_name.value: args.app or self.default_app,
            Args.keywords.value: args.keywords or self.default_keywords,
            Args.tags.value: args.tags or self.default_tags,
            Args.reruns.value: args.rerun or self.default_rerun,
            Args.record_failed_case.value: args.record_failed_case or self.default_record_failed_case,
            Args.clean.value: args.clean or self.default_clean,
            Args.report_formats.value: args.report_formats
                                       or self.default_report_formats,
            Args.max_fail.value: args.max_fail or self.default_max_fail,
            Args.log_level.value: args.log_level or self.default_log_level,
            Args.timeout.value: args.timeout or self.default_timeout,
            Args.debug.value: args.debug or self.default_debug,
            Args.noskip.value: args.noskip or self.default_noskip,
            Args.ifixed.value: args.ifixed or self.default_ifixed,
            Args.send_pms.value: args.send_pms or self.default_send_pms,
            Args.task_id.value: args.task_id or self.default_task_id,
            Args.trigger.value: args.trigger or self.default_trigger,
            Args.resolution.value: args.resolution or self.default_resolution,
            Args.case_file.value: args.case_file or self.default_case_file,
            Args.deb_path.value: args.deb_path or self.default_deb_path,
            Args.pms_user.value: args.pms_user or self.default_pms_user,
            Args.pms_password.value: args.pms_password or self.default_pms_password,
            Args.suite_id.value: args.suite_id or self.default_suite_id,
            Args.pms_info_file.value: args.pms_info_file or self.default_pms_info_file,
            Args.top.value: args.top or self.default_top,
            Args.lastfailed.value: args.lastfailed or self.default_lastfailed,
            Args.duringfail.value: args.duringfail or self.default_duringfail,
            Args.repeat.value: args.repeat or self.default_repeat,
            Args.project_name.value: args.project_name or self.default_project_name,
            Args.build_location.value: args.build_location or self.default_build_location,
            Args.line.value: args.line or self.default_line,
            Args.autostart.value: args.autostart or self.default_autostart,
        }
        if local_kwargs.get(Args.autostart.value) or GlobalConfig.AUTOSTART:
            import letmego
            letmego.conf.setting.PASSWORD = GlobalConfig.PASSWORD
            letmego.register_autostart_service(
                user=GlobalConfig.USERNAME,
                working_directory=GlobalConfig.ROOT_DIR,
                cmd=f"pipenv run python manage.py {' '.join(self.cmd_args)}"
            )
        return local_kwargs, args

    def pms_control(self, parser=None, sub_parser_pms=None):
        """pms相关功能命令行参数"""
        sub_parser_pms.add_argument(
            "-a", "--app", default="",
            help="应用名称：apps/autotest_deepin_music 或 autotest_deepin_music"
        )
        sub_parser_pms.add_argument(
            "-u", "--pms_user", default="", help="pms 用户名"
        )
        sub_parser_pms.add_argument(
            "-p", "--pms_password", default="", help="pms 密码"
        )
        sub_parser_pms.add_argument(
            "-plc", "--pms_link_csv", default="",
            help="pms 和 csv 的映射关系，比如：music:81/album:82，多个配置使用'/'分隔"
        )
        sub_parser_pms.add_argument(
            "-p2c", "--pms2csv", action='store_const', const=True, default=False,
            help="从PMS爬取用例标签到csv文件"
        )
        sub_parser_pms.add_argument(
            "--send2task",
            choices=["yes", ""],
            default="", help="回填数据到pms测试单"
        )
        sub_parser_pms.add_argument(
            "--task_id", default="", help="测试单ID"
        )
        sub_parser_pms.add_argument(
            "--trigger", choices=["auto", "hand", ""], default="",
            help="触发者"
        )
        args = parser.parse_args()
        pms_kwargs = {
            Args.app_name.value: args.app or self.default_app,
            Args.pms_user.value: args.pms_user or self.default_pms_user,
            Args.pms_password.value: args.pms_password or self.default_pms_password,
            Args.pms2csv.value: args.pms2csv or self.default_pms2csv,
            Args.pms_link_csv.value: args.pms_link_csv or self.default_pms_link_csv,
            Args.send2task.value: args.send2task or self.default_send2task,
            Args.task_id.value: args.task_id or GlobalConfig.TASK_ID,
            Args.trigger.value: args.trigger or GlobalConfig.TRIGGER,
        }
        if pms_kwargs.get(Args.pms2csv.value):
            Pms2Csv(
                app_name=pms_kwargs.get(Args.app_name.value),
                user=pms_kwargs.get(Args.pms_user.value) or GlobalConfig.PMS_USER,
                password=pms_kwargs.get(Args.pms_password.value) or GlobalConfig.PMS_PASSWORD,
                pms_link_csv=pms_kwargs.get(Args.pms_link_csv.value),
            ).write_new_csv()
        elif (
                pms_kwargs.get(Args.send2task.value)
                and pms_kwargs.get(Args.task_id.value)
                and pms_kwargs.get(Args.trigger.value) == "hand"
        ):
            Send2Pms().send2pms(
                Send2Pms.case_res_path(pms_kwargs.get(Args.task_id.value)),
                Send2Pms.data_send_result_csv(pms_kwargs.get(Args.trigger.value))
            )
        else:
            raise ValueError

    @staticmethod
    def start_app(startapp=None):
        """新建app工程"""
        if startapp:
            start = StartApp(startapp)
            start.copy_template_to_apps()
            start.rewrite()

    def csv_control(self, parser=None, sub_parser_csv=None):
        """csv相关功能命令参数"""
        sub_parser_csv.add_argument(
            "-a", "--app", default="",
            help="应用名称：apps/autotest_deepin_music 或 autotest_deepin_music"
        )
        sub_parser_csv.add_argument(
            "-k", "--keywords", default="", help="用例的关键词"
        )
        sub_parser_csv.add_argument(
            "-t", "--tags", default="", help="用例的标签"
        )
        sub_parser_csv.add_argument(
            "-p2c", "--pyid2csv", action='store_const', const=True, default=False,
            help="将用例py文件的case id同步到对应的csv文件中"
        )
        sub_parser_csv.add_argument(
            "-ec", "--export_csv_file", default="", help="导出csv文件名称，比如：case_list.csv"
        )
        args = parser.parse_args()
        csv_kwargs = {
            Args.app_name.value: args.app or self.default_app,
            Args.keywords.value: args.keywords or self.default_keywords,
            Args.tags.value: args.tags or self.default_tags,
            Args.pyid2csv.value: args.pyid2csv or self.default_pyid2csv or GlobalConfig.PY_ID_TO_CSV,
            Args.export_csv_file.value: args.export_csv_file or self.default_export_csv_file,
            "collection_only": True
        }
        if csv_kwargs.get(Args.pyid2csv.value) or GlobalConfig.PY_ID_TO_CSV:
            from src.csvctl import CsvControl
            _csv = CsvControl(csv_kwargs.get(Args.app_name.value))
            _csv.delete_mark_in_csv_if_not_exists_py()
            _csv.async_mark_to_csv()
        elif csv_kwargs.get(Args.export_csv_file.value):
            LocalRunner(**csv_kwargs).local_run()
        else:
            logger.error(
                f"需要传递一些有用参数或配置项：{Args.pyid2csv.value} 或 {Args.export_csv_file.value}"
                "，您可以使用 -h 或 --help 查看支持的参数"
            )


if __name__ == "__main__":
    try:
        Manage()
    except Exception as exc:
        traceback.print_exception(*sys.exc_info())
