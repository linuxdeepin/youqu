import click

from youqu3 import version

_slaves_help = """\
用例步骤中与其他机器进行交互 -s/--slaves ${user}@${ip}:${password}
如：-s mikigo@192.168.8.11:admin123
如果${password}和前面配置项PASSWORD一样，可以不传：${user}@${ip}
多个机器之间用斜线分割：${user}@${ip}:${password}/${user}@${ip}
"""


@click.group()
@click.help_option("-h", "--help", help="查看帮助信息")
@click.version_option(version, "-v", "--version", prog_name="YouQu3", help="查看版本号")
def cli(): ...


@cli.command()
@click.help_option("-h", "--help", help="查看帮助信息")
@click.option("-w", "--workdir", default=None, type=click.STRING,
              help="工作目录")
@click.option("-p", "--path", default=None, type=click.STRING,
              help="指定用例文件或目录路径执行，")
@click.option("-k", "--keywords", default=None, type=click.STRING,
              help="指定用例关键词执行，支持 'and/or/not' 逻辑表达式")
@click.option("-t", "--tags", default=None, type=click.STRING,
              help="指定用例标签执行，支持 'and/or/not' 逻辑表达式")
@click.option("--setup-plan", is_flag=True, default=False, help="")
@click.option("-s", "--slaves", default=None, type=click.STRING, help=_slaves_help)
@click.option("--txt", is_flag=True, default=False, type=click.BOOL,
              help="基于txt文件执行用例：youqu-tags.txt or youqu-keywords.txt")
@click.option("--reruns", default=None, type=click.STRING, help="重跑次数")
@click.option("--job-start", default=None, type=click.STRING, help="测试结束之前执行")
@click.option("--job-end", default=None, type=click.STRING, help="测试结束之后执行")
@click.option("--pytest-opt", default=None, type=click.STRING, help="pytest命令行参数")
@click.option("--record-failed-num", default=None, type=click.STRING, help="从第几次重跑开始录屏")
def run(
        workdir,
        path,
        keywords,
        tags,
        setup_plan,
        slaves,
        txt,
        reruns,
        job_start,
        job_end,
        pytest_opt,
        record_failed_num,
):
    """本地执行"""
    args = {
        "workdir": workdir,
        "path": path,
        "keywords": keywords,
        "tags": tags,
        "setup_plan": setup_plan,
        "slaves": slaves,
        "txt": txt,
        "reruns": reruns,
        "job_start": job_start,
        "job_end": job_end,
        "pytest_opt": pytest_opt,
        "record_failed_num": record_failed_num,
    }
    from youqu3.driver.run import Run
    Run(**args).run()


@cli.command()
@click.help_option("-h", "--help", help="查看帮助信息")
@click.option("-c", "--clients", default=None, type=click.STRING,
              help="远程机器信息:user@ip:password，多个机器之间用 '/' 连接")
@click.option("-w", "--workdir", default=None, type=click.STRING,
              help="工作目录")
@click.option("-p", "--path", default=None, type=click.STRING,
              help="指定用例文件路径执行")
@click.option("-k", "--keywords", default=None, type=click.STRING,
              help="指定用例关键词执行，支持 'and/or/not' 逻辑表达式")
@click.option("-t", "--tags", default=None, type=click.STRING,
              help="指定用例标签执行，支持 'and/or/not' 逻辑表达式")
@click.option("-s", "--slaves", default=None, type=click.STRING, help=_slaves_help)
@click.option("--txt", is_flag=True, default=False, type=click.BOOL,
              help="基于txt文件执行用例：youqu-tags.txt or youqu-keywords.txt")
@click.option("--reruns", default=None, type=click.STRING, help="重跑次数")
@click.option("--job-start", default=None, type=click.STRING, help="测试结束之前执行")
@click.option("--job-end", default=None, type=click.STRING, help="测试结束之后执行")
@click.option("--pytest-opt", default=None, type=click.STRING, help="pytest命令行参数")
@click.option("--record-failed-num", default=None, type=click.STRING, help="从第几次重跑开始录屏")
def remote(
        clients,
        workdir,
        path,
        keywords,
        tags,
        slaves,
        txt,
        reruns,
        job_start,
        job_end,
        pytest_opt,
        record_failed_num,
):
    """远程控制执行"""
    args = {
        "clients": clients,
        "workdir": workdir,
        "path": path,
        "keywords": keywords,
        "tags": tags,
        "slaves": slaves,
        "txt": txt,
        "reruns": reruns,
        "job_start": job_start,
        "job_end": job_end,
        "pytest_opt": pytest_opt,
        "record_failed_num": record_failed_num,
    }
    from youqu3.driver.remote import Remote
    Remote(**args).run()


@cli.command()
def init():
    """创建用例工程"""
    from youqu3.driver.init import Init
    from youqu3.driver.init import print_tree
    Init().init()
    print_tree()


@cli.command()
@click.help_option("-h", "--help", help="查看帮助信息")
@click.option("--python", default="3", type=click.STRING, help="指定虚拟环境的Python版本")
def envx(python):
    """虚拟环境安装"""
    from youqu3.driver.envx import envx as env
    env(python_version=python)


if __name__ == '__main__':
    cli()
