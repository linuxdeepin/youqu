#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only

import functools
import os
import sys
import time

from os.path import dirname
from os.path import basename

sys.path.append(dirname(dirname(dirname(os.path.abspath(__file__)))))

try:
    import zerorpc
except ImportError:
    os.system("pip3 install zerorpc -i https://pypi.tuna.tsinghua.edu.cn/simple")
    time.sleep(1)
    import zerorpc




def _context_manager(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        tool_status = os.popen(
            f'''sshpass -p '{conf.PASSWORD}' ssh {kwargs['user']}@{kwargs['ip']} "ps -aux |  grep {basename(__file__)} | grep -v grep"'''
        ).read()
        if not tool_status:
            client_project_path = "/".join(conf.ROOT_DIR.split("/")[3:])
            sudo = f"echo '{conf.PASSWORD}' | sudo -S"

            if "StrictHostKeyChecking no" not in os.popen("cat /etc/ssh/ssh_config").read():
                os.system(
                    f'{sudo} sed -i "s/#   StrictHostKeyChecking ask/ StrictHostKeyChecking no/g" /etc/ssh/ssh_config'
                )
            if "/home/" not in conf.ROOT_DIR:
                raise EnvironmentError

            os.system(
                f'''sshpass -p '{conf.PASSWORD}' ssh {kwargs['user']}@{kwargs['ip']} "mkdir -p ~/{client_project_path}"''')
            exclude = ""
            for i in [
                "apps",
                "report",
                "public",
                "__pycache__",
                ".pytest_cache",
                ".vscode",
                ".idea",
                ".git",
                "site",
                "docs",
                "site",
                "README.md",
                "README.en.md",
                "RELEASE.md",
            ]:
                exclude += f"--exclude='{i}' "
            os.system(
                f"sshpass -p '{conf.PASSWORD}' rsync -av -e ssh {exclude} {conf.ROOT_DIR}/* "
                f"{kwargs['user']}@{kwargs['ip']}:~/{client_project_path}/"
            )
            os.system(
                f"sshpass -p '{conf.PASSWORD}' ssh {kwargs['user']}@{kwargs['ip']} "
                f'"cd ~/{client_project_path}/ && '
                f'bash env.sh"'
            )
            _cmd = (
                f"nohup sshpass -p '{conf.PASSWORD}' ssh {kwargs['user']}@{kwargs['ip']} "
                f'"cd ~/{client_project_path}/src/remotectl/ && '
                f'pipenv run python {basename(__file__)}" > /tmp/{basename(__file__)}.log 2>&1 &'
            )
            print(_cmd)
            res = os.popen(_cmd).read()
            print(res)
            time.sleep(2)
        return func(*args, **kwargs)

    return wrapper


@_context_manager
def remote_dogtail_ctl(user=None, ip=None, password=None, app_name=None, desc=None, **kwargs):
    r = zerorpc.Client(timeout=50, heartbeat=None)
    r.connect(f"tcp://{ip}:4242")
    return r


if __name__ == '__main__':
    from os import environ
    from setting import conf
    environ["XAUTHORITY"] = f"/home/{conf.USERNAME}/.Xauthority"
    from src.dogtail_utils import DogtailUtils

    server = zerorpc.Server(DogtailUtils())
    server.bind("tcp://0.0.0.0:4242")
    server.run()
