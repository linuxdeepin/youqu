def git_control(self, parser=None, sub_parser_git=None):
    sub_parser_git.add_argument(
        "-a",
        "--app",
        default="",
        help="应用名称：apps/autotest_deepin_music 或 autotest_deepin_music",
    )
    sub_parser_git.add_argument("-u", "--user", default="", help="git仓库用户名")
    sub_parser_git.add_argument("-p", "--password", default="", help="git仓库地密码")
    sub_parser_git.add_argument("-l", "--url", default="", help="git仓库地址")
    sub_parser_git.add_argument("-b", "--branch_or_tag", default="", help="分支或Tag")
    sub_parser_git.add_argument("-d", "--depth", default="", help="git仓库克隆深度")
    sub_parser_git.add_argument("-s", "--startdate", default="", help="统计开始时间")
    sub_parser_git.add_argument("-e", "--enddate", default="", help="统计结束时间")
    args = parser.parse_args()
    from src.rtk._base import Args

    git_kwargs = {
        Args.app_name.value: args.app or self.default_app,
        Args.url.value: args.url or self.default_url,
        Args.user.value: args.user or self.default_git_user,
        Args.password.value: args.password or self.default_git_password,
        Args.branch.value: args.branch or self.default_branch,
        Args.depth.value: args.depth or self.default_depth,
        Args.startdate.value: args.startdate or self.default_startdate,
        Args.enddate.value: args.enddate or self.default_enddate,
    }
    from src.git.check import check_git_installed

    if git_kwargs.get(Args.url.value):
        if all(
            [
                git_kwargs.get(Args.user.value),
                git_kwargs.get(Args.password.value),
            ]
        ):
            from src.git.clone import sslclone as git_clone
        else:
            from src.git.clone import clone as git_clone
        check_git_installed()
        git_clone(**git_kwargs)
    if all(
        [
            git_kwargs.get(Args.app_name.value),
            git_kwargs.get(Args.startdate.value),
        ]
    ):
        from src.git.code_statistics import CodeStatistics

        check_git_installed()
        CodeStatistics(**git_kwargs).codex()
