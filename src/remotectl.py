#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

import functools
# SPDX-License-Identifier: GPL-2.0-only
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from setting import conf

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
            f'''sshpass -p '{conf.PASSWORD}' ssh {kwargs['user']}@{kwargs['ip']} "ps -aux |  grep remote_mousekey | grep -v grep"'''
        ).read()
        if not tool_status:
            sudo = f"echo '{conf.PASSWORD}' | sudo -S"
            if "StrictHostKeyChecking no" not in os.popen("cat /etc/ssh/ssh_config").read():
                os.system(
                    f'{sudo} sed -i "s/#   StrictHostKeyChecking ask/ StrictHostKeyChecking no/g" /etc/ssh/ssh_config'
                )
            if "/home/" not in conf.ROOT_DIR:
                raise EnvironmentError
            client_project_path = "/".join(conf.ROOT_DIR.split("/")[3:])
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
                f'"cd ~/{client_project_path}/;'
                f'bash env.sh"'
            )
            _cmd = (
                f"nohup sshpass -p '{conf.PASSWORD}' ssh {kwargs['user']}@{kwargs['ip']} "
                f'"cd ~/{client_project_path}/src/;'
                f'pipenv run python remotectl.py" > /tmp/remote_result.log 2>&1 &'
            )
            print(_cmd)
            res = os.popen(_cmd).read()
            print(res)
            time.sleep(2)
        return func(*args, **kwargs)

    return wrapper


@_context_manager
def remotectl(user, ip):
    r = zerorpc.Client(timeout=50, heartbeat=None)
    r.connect(f"tcp://{ip}:4242")
    return r


if __name__ == '__main__':
    from src import Src

    server = zerorpc.Server(Src())
    server.bind("tcp://0.0.0.0:4242")
    server.run()
