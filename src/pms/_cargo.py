from setting.globalconfig import GlobalConfig


def pms_control(parser=None, sub_parser_pms=None):
    """pms相关功能命令行参数"""
    sub_parser_pms.add_argument(
        "-a",
        "--app",
        default="",
        help="应用名称：apps/autotest_deepin_music 或 autotest_deepin_music",
    )
    sub_parser_pms.add_argument("-u", "--pms_user", default="", help="pms 用户名")
    sub_parser_pms.add_argument("-p", "--pms_password", default="", help="pms 密码")
    sub_parser_pms.add_argument(
        "-plc",
        "--pms_link_csv",
        default="",
        help="pms 和 csv 的映射关系，比如：music:81/album:82，多个配置使用'/'分隔",
    )
    sub_parser_pms.add_argument(
        "-p2c",
        "--pms2csv",
        action="store_const",
        const=True,
        default=False,
        help="从PMS爬取用例标签到csv文件",
    )
    sub_parser_pms.add_argument(
        "--send2task", choices=["yes", ""], default="", help="回填数据到pms测试单"
    )
    sub_parser_pms.add_argument("--task_id", default="", help="测试单ID")
    sub_parser_pms.add_argument(
        "--trigger", choices=["auto", "hand", ""], default="", help="触发者"
    )
    args = parser.parse_args()
    from src.rtk._base import Args

    pms_kwargs = {
        Args.app_name.value: args.app,
        Args.pms_user.value: args.pms_user,
        Args.pms_password.value: args.pms_password,
        Args.pms2csv.value: args.pms2csv,
        Args.pms_link_csv.value: args.pms_link_csv,
        Args.send2task.value: args.send2task,
        Args.task_id.value: args.task_id or GlobalConfig.TASK_ID,
        Args.trigger.value: args.trigger or GlobalConfig.TRIGGER,
    }
    if pms_kwargs.get(Args.pms2csv.value):
        from src.pms.pms2csv import Pms2Csv

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
        from src.pms.send2pms import Send2Pms

        Send2Pms().send2pms(
            Send2Pms.case_res_path(pms_kwargs.get(Args.task_id.value)),
            Send2Pms.data_send_result_csv(pms_kwargs.get(Args.task_id.value)),
        )
    else:
        raise ValueError
