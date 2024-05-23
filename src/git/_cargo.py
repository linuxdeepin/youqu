def git_control(parser=None, sub_parser_git=None):
    sub_parser_git.add_argument(
        "-a",
        "--app",
        default="",
        help="应用名称：apps/autotest_deepin_music 或 autotest_deepin_music",
    )
    sub_parser_git.add_argument("-u", "--git_user", default="", help="git仓库用户名")
    sub_parser_git.add_argument("-p", "--git_password", default="", help="git仓库地密码")
    sub_parser_git.add_argument("-l", "--git_url", default="", help="git仓库地址")
    sub_parser_git.add_argument("-b", "--branch_or_tag", default="", help="分支或Tag")
    sub_parser_git.add_argument("-d", "--depth", default="", help="git仓库克隆深度")
    sub_parser_git.add_argument("-s", "--startdate", default="", help="统计开始时间")
    sub_parser_git.add_argument("-e", "--enddate", default="", help="统计结束时间")
    args = parser.parse_args()
    from src.rtk._base import Args
    from setting import conf

    git_kwargs = {
        Args.app_name.value: args.app or conf.APP_NAME,
        Args.git_url.value: args.git_url or conf.GIT_URL,
        Args.git_user.value: args.git_user or conf.GIT_USER,
        Args.git_password.value: args.git_password or conf.GIT_PASSWORD,
        Args.branch.value: args.branch_or_tag or conf.BRANCH,
        Args.depth.value: args.depth or conf.DEPTH,
        Args.startdate.value: args.startdate or conf.START_DATE,
        Args.enddate.value: args.enddate or conf.END_DATE,
    }
    from src.git.check import check_git_installed

    if git_kwargs.get(Args.git_url.value):
        if all(
            [
                git_kwargs.get(Args.git_user.value),
                git_kwargs.get(Args.git_password.value),
            ]
        ):
            from src.git.clone import sslclone as git_clone
        else:
            from src.git.clone import clone as git_clone
        check_git_installed()
        git_clone(**git_kwargs)
    if git_kwargs.get(Args.app_name.value):
        if git_kwargs.get(Args.startdate.value):
            from src.git.code_statistics import CodeStatistics

            check_git_installed()
            CodeStatistics(**git_kwargs).codex()
        else:
            print("-s/--startdate 参数未传入")
    else:
        print("-a/--app 参数未传入")
