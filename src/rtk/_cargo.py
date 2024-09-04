from funnylog import logger

from setting.globalconfig import GlobalConfig


def local_runner(parser, sub_parser_run, cmd_args=None):
    """本地执行"""
    sub_parser_run.add_argument(
        "-a",
        "--app",
        default="",
        help="应用名称：apps/autotest_deepin_music 或 autotest_deepin_music",
    )
    sub_parser_run.add_argument(
        "-k", "--keywords", default="", help="用例的关键词,支持and/or/not逻辑组合"
    )
    sub_parser_run.add_argument(
        "-t", "--tags", default="", help="用例的标签,支持and/or/not逻辑组合"
    )
    sub_parser_run.add_argument("--rerun", default="", help="失败重跑次数")
    sub_parser_run.add_argument(
        "--record_failed_case", default="", help="失败录屏从第几次失败开始录制视频"
    )
    sub_parser_run.add_argument("--clean", choices=["yes", ""], default="", help="清理环境")
    sub_parser_run.add_argument("--report_formats", default="", help="测试报告格式")
    sub_parser_run.add_argument("--max_fail", default="", help="最大失败率")
    sub_parser_run.add_argument("--log_level", default="", help="日志输出级别")
    sub_parser_run.add_argument("--timeout", default="", help="单条用例超时时间")
    sub_parser_run.add_argument("--resolution", default="", help="检查分辨率")
    sub_parser_run.add_argument("--debug", default="", help="调试模式")
    sub_parser_run.add_argument(
        "--noskip",
        choices=["yes", ""],
        default="",
        help="csv文件里面标记了skip跳过的用例不生效",
    )
    sub_parser_run.add_argument(
        "--ifixed", choices=["yes", ""], default="", help="fixed不生效，仅通过skip跳过用例"
    )
    sub_parser_run.add_argument(
        "--send_pms", choices=["", "async", "finish"], default="", help="数据回填"
    )
    sub_parser_run.add_argument("--task_id", default="", help="测试单ID")
    sub_parser_run.add_argument(
        "--trigger", choices=["", "auto", "hand"], default="", help="触发者"
    )
    sub_parser_run.add_argument("-f", "--case_file", default="", help="根据文件执行用例")
    sub_parser_run.add_argument("--deb_path", default="", help="需要安装deb包的本地路径")
    sub_parser_run.add_argument("-u", "--pms_user", default="", help="pms 用户名")
    sub_parser_run.add_argument("-p", "--pms_password", default="", help="pms 密码")
    sub_parser_run.add_argument("--suite_id", default="", help="pms 测试套ID")
    sub_parser_run.add_argument("--pms_info_file", default="", help="pms 信息文件")
    sub_parser_run.add_argument("--top", default="", help="过程中记录top命令中的值")
    sub_parser_run.add_argument(
        "--lastfailed",
        action="store_const",
        const=True,
        default=False,
        help="仅执行上次失败用例",
    )
    sub_parser_run.add_argument(
        "--duringfail",
        action="store_const",
        const=True,
        default=False,
        help="测试过程中立即显示报错",
    )
    sub_parser_run.add_argument("--repeat", default="", help="指定用例执行次数")
    sub_parser_run.add_argument("--project_name", default="", help="工程名称（写入json文件）")
    sub_parser_run.add_argument("--build_location", default="", help="构建地区（写入json文件）")
    sub_parser_run.add_argument("--line", default="", help="执行的业务线（写入json文件）")
    sub_parser_run.add_argument("--autostart", default="", help="重启类场景开启letmego执行方案")
    sub_parser_run.add_argument("--slaves", default="", help="远程测试机")
    args = parser.parse_args()
    from src.rtk._base import Args

    local_kwargs = {
        Args.app_name.value: args.app,
        Args.keywords.value: args.keywords,
        Args.tags.value: args.tags,
        Args.reruns.value: args.rerun,
        Args.record_failed_case.value: args.record_failed_case,
        Args.clean.value: args.clean,
        Args.report_formats.value: args.report_formats,
        Args.max_fail.value: args.max_fail,
        Args.log_level.value: args.log_level,
        Args.timeout.value: args.timeout,
        Args.debug.value: args.debug,
        Args.noskip.value: args.noskip,
        Args.ifixed.value: args.ifixed,
        Args.send_pms.value: args.send_pms,
        Args.task_id.value: args.task_id,
        Args.trigger.value: args.trigger,
        Args.resolution.value: args.resolution,
        Args.case_file.value: args.case_file,
        Args.deb_path.value: args.deb_path,
        Args.pms_user.value: args.pms_user,
        Args.pms_password.value: args.pms_password,
        Args.suite_id.value: args.suite_id,
        Args.pms_info_file.value: args.pms_info_file,
        Args.top.value: args.top,
        Args.lastfailed.value: args.lastfailed,
        Args.duringfail.value: args.duringfail,
        Args.repeat.value: args.repeat,
        Args.project_name.value: args.project_name,
        Args.build_location.value: args.build_location,
        Args.line.value: args.line,
        Args.autostart.value: args.autostart,
        Args.slaves.value: args.slaves,
    }
    if local_kwargs.get(Args.autostart.value) or GlobalConfig.AUTOSTART:
        try:
            import letmego

            letmego.conf.setting.PASSWORD = GlobalConfig.PASSWORD
            letmego.register_autostart_service(
                user=GlobalConfig.USERNAME,
                working_directory=GlobalConfig.ROOT_DIR,
                cmd=f"pipenv run python manage.py {' '.join(cmd_args)}",
            )
        except ModuleNotFoundError:
            ...
    return local_kwargs, args


def remote_runner(parser, sub_parser_remote):
    sub_parser_remote.add_argument(
        "-c",
        "--clients",
        default="",
        help=(
            "远程机器的user@ip:password,多个机器用'/'连接,"
            "如果password不传入,默认取setting/remote.ini中CLIENT_PASSWORD的值,"
            "比如: uos@10.8.13.xx:1 或 uos@10.8.13.xx"
        ),
    )
    sub_parser_remote.add_argument(
        "-s",
        "--send_code",
        action="store_const",
        const=True,
        default=False,
        help="发送代码到测试机（不含report目录）",
    )
    sub_parser_remote.add_argument(
        "-e",
        "--build_env",
        action="store_const",
        const=True,
        default=False,
        help="搭建测试环境,如果为yes，不管send_code是否为yes都会发送代码到测试机.",
    )
    sub_parser_remote.add_argument(
        "-cp", "--client_password", default="", help="测试机密码（全局）"
    )
    sub_parser_remote.add_argument(
        "--git_url", default="", help="git仓库地址"
    )
    sub_parser_remote.add_argument(
        "--git_user", default="", help="git仓库用户名"
    )
    sub_parser_remote.add_argument(
        "--git_password", default="", help="git仓库密码"
    )
    sub_parser_remote.add_argument(
        "-b", "--branch_or_tag", default="", help="分支或Tag"
    )
    sub_parser_remote.add_argument(
        "-d", "--depth", default="", help="git仓库克隆深度"
    )
    sub_parser_remote.add_argument(
        "-y",
        "--parallel",
        default="",
        help=(
            "yes:表示所有测试机并行跑，执行相同的测试用例;"
            "no:表示测试机分布式执行，服务端会根据收集到的测试用例自动分配给各个测试机执行。"
        ),
    )
    sub_parser_remote.add_argument(
        "--json_backfill_base_url", default="", help="json报告回填的接口地址"
    )
    sub_parser_remote.add_argument(
        "--json_backfill_task_id", default="", help="json报告回填所属任务id"
    )
    sub_parser_remote.add_argument(
        "--json_backfill_user", default="", help="json报告回填的用户名"
    )
    sub_parser_remote.add_argument(
        "--json_backfill_password", default="", help="json报告回填的密码"
    )
    sub_parser_remote.add_argument(
        "--json_backfill_custom_api", default="", help="json报告回填的自定义api，默认是/api/youqu/yqresult/"
    )

    local_kwargs, args = local_runner(parser, sub_parser_remote)
    from src.rtk._base import Args

    remote_kwargs = {
        Args.clients.value: args.clients,
        Args.send_code.value: args.send_code,
        Args.build_env.value: args.build_env,
        Args.client_password.value: args.client_password,
        Args.git_url.value: args.git_url or GlobalConfig.GIT_URL,
        Args.git_user.value: args.git_user or GlobalConfig.GIT_USER,
        Args.git_password.value: args.git_password or GlobalConfig.GIT_PASSWORD,
        Args.branch.value: args.branch_or_tag or GlobalConfig.BRANCH,
        Args.depth.value: args.depth or GlobalConfig.DEPTH,
        Args.parallel.value: args.parallel,
        Args.json_backfill_base_url.value: args.json_backfill_base_url,
        Args.json_backfill_task_id.value: args.json_backfill_task_id,
        Args.json_backfill_user.value: args.json_backfill_user,
        Args.json_backfill_password.value: args.json_backfill_password,
        Args.json_backfill_custom_api.value: args.json_backfill_custom_api,
    }
    _remote_kwargs = {
        "remote_kwargs": remote_kwargs,
        "local_kwargs": local_kwargs,
    }

    if remote_kwargs.get(Args.git_url.value):
        if all(
                [
                    remote_kwargs.get(Args.git_user.value),
                    remote_kwargs.get(Args.git_password.value),
                ]
        ):
            from src.git.clone import sslclone as git_clone
        else:
            from src.git.clone import clone as git_clone
        from src.git.check import check_git_installed
        check_git_installed()
        git_clone(**remote_kwargs)
    return _remote_kwargs


def csv_control(parser=None, sub_parser_csv=None):
    sub_parser_csv.add_argument(
        "-a",
        "--app",
        default="",
        help="应用名称：apps/autotest_deepin_music 或 autotest_deepin_music",
    )
    sub_parser_csv.add_argument("-k", "--keywords", default="", help="用例的关键词")
    sub_parser_csv.add_argument("-t", "--tags", default="", help="用例的标签")
    sub_parser_csv.add_argument(
        "-p2c",
        "--pyid2csv",
        action="store_const",
        const=True,
        default=False,
        help="将用例py文件的case id同步到对应的csv文件中",
    )
    sub_parser_csv.add_argument(
        "-ec", "--export_csv_file", default="", help="导出csv文件名称，比如：case_list.csv"
    )
    args = parser.parse_args()
    from src.rtk._base import Args

    csv_kwargs = {
        Args.app_name.value: args.app,
        Args.keywords.value: args.keywords,
        Args.tags.value: args.tags,
        Args.pyid2csv.value: args.pyid2csv,
        Args.export_csv_file.value: args.export_csv_file,
        "collection_only": True,
    }
    if csv_kwargs.get(Args.pyid2csv.value) or GlobalConfig.PY_ID_TO_CSV:
        from src.csvctl import CsvControl

        _csv = CsvControl(csv_kwargs.get(Args.app_name.value))
        _csv.delete_mark_in_csv_if_not_exists_py()
        _csv.async_mark_to_csv()
    elif csv_kwargs.get(Args.export_csv_file.value):
        from src.rtk.local_runner import LocalRunner

        LocalRunner(**csv_kwargs).local_run()
    else:
        logger.error(
            f"需要传递一些有用参数或配置项：{Args.pyid2csv.value} 或 {Args.export_csv_file.value}"
            "，您可以使用 -h 或 --help 查看支持的参数"
        )
