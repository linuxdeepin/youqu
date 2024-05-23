from enum import Enum
from enum import unique
from setting.globalconfig import GlobalConfig


def help_tip():
    color = "32"
    return (
        f'''\033[1;{color}mYouQu\033[0m 支持的子命令:\n    '''
        f'''\033[1;{color}m{str([i.value for i in SubCmd]).replace("'", "").strip("[").strip("]")}\033[0m'''
        f"\n您需要传入其中一个子命令,可以使用 \033[1;{color}m-h\033[0m 或 \033[1;{color}m--help\033[0m 查看每个命令参数的详细使用说明."
        f"\n如: \033[1;{color}myouqu manage.py run -h\033[0m \n"
    )


def start_app(startapp=None):
    if startapp:
        from src.startapp import StartApp

        start = StartApp(startapp)
        start.copy_template_to_apps()
        start.rewrite()


def trim():
    from src.depends.cfonts import say

    say(GlobalConfig.PROJECT_NAME)
    version_font = "slick"
    color = "32"
    say(GlobalConfig.current_tag, font=version_font, space=False)
    say(f"Code: \033[1;{color}m{GlobalConfig.GITHUB_URL}\033[0m", font="console", space=False)
    say(f"Docs: \033[1;{color}m{GlobalConfig.DOCS_URL}\033[0m", font="console", space=False)
    say(f"PyPI: \033[1;{color}m{GlobalConfig.PyPI_URL}\033[0m", font="console", space=False)
    say(f'\033[1;{color}m{"=" * 60}\033[0m', font="console", space=False)


@unique
class SubCmd(Enum):
    run = "run"
    remote = "remote"
    pmsctl = "pmsctl"
    csvctl = "csvctl"
    startapp = "startapp"
    git = "git"
