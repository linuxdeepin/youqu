import os.path
import pathlib

from youqu3 import exceptions
from youqu3 import logger
from youqu3 import setting
from youqu3.cmd import Cmd


def cli_cmd_creator(cmd_name, cmd_txt):
    cmd_path = os.path.expanduser(f"~/.local/bin/{cmd_name}")
    if not os.path.exists(cmd_path):
        Cmd.run(f"echo '{cmd_txt}' >> {cmd_path}")
        Cmd.run(f"chmod +x {cmd_path}")


def envx(python_version=None):
    if python_version is None:
        python_version = "3"
    rootdir = pathlib.Path(".").absolute()
    logger.info(rootdir)
    # pip
    _, return_code = Cmd.run("pip3 --version", return_code=True)
    if return_code != 0:
        Cmd.run(
            'curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py && && python3 get-pip.py',
            timeout=600
        )
    # youqu3
    Cmd.run(f'pip3 install youqu3 -i {setting.PYPI_MIRROR}')
    # youqu3-cargo
    cli_cmd_creator("youqu3-cargo", 'pipenv run youqu3 "$@"')
    # youqu3-shell
    cli_cmd_creator("youqu3-shell", 'pipenv shell')
    # youqu3-rm
    cli_cmd_creator("youqu3-rm", 'pipenv --rm')
    # PATH
    with open(os.path.expanduser("~/.bashrc"), 'r') as f:
        bashrc = f.read()
    path_cmd = "export PATH=$PATH:$HOME/.local/bin"
    if path_cmd not in bashrc:
        Cmd.run(f"echo '{path_cmd}' >> ~/.bashrc")
        Cmd.run("source ~/.bashrc")
    # pipenv
    Cmd.run(f'pip3 install pipenv -i {setting.PYPI_MIRROR}')
    Cmd.run(f"cd {rootdir} && pipenv --python {python_version}")
    os.system(
        f"cd {rootdir} && pipenv run pip install -r requirements.txt -i {setting.PYPI_MIRROR}",
    )


if __name__ == '__main__':
    envx()
