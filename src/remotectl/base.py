#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only

import functools
import os
import subprocess
import sys
import time
import multiprocessing

from os.path import dirname
from os.path import basename

sys.path.append(dirname(dirname(dirname(os.path.abspath(__file__)))))

from setting import conf
from src.depends.colorama import Fore

client_project_path = "/".join(conf.ROOT_DIR.split("/")[3:])
exclude_files = [
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
]


def _feeling_good(cmd):
    subprocess.Popen(cmd, shell=True)


def _base_env_check(password):
    sudo = f"echo '{password}' | sudo -S"
    if "StrictHostKeyChecking no" not in os.popen("cat /etc/ssh/ssh_config").read():
        os.system(
            f'{sudo} sed -i "s/#   StrictHostKeyChecking ask/ StrictHostKeyChecking no/g" /etc/ssh/ssh_config'
        )
    if "/home/" not in conf.ROOT_DIR:
        raise EnvironmentError


def _exclude():
    exclude_str = ""
    for i in exclude_files:
        exclude_str += f"--exclude='{i}' "

    return exclude_str


def _transfer_to_client(ip, password, user, filename, transfer_appname=None):
    os.system(
        f'''sshpass -p '{password}' ssh {user}@{ip} "mkdir -p ~/{client_project_path}"'''
    )
    os.system(
        f"sshpass -p '{password}' rsync -av -e ssh {_exclude()} {conf.ROOT_DIR}/* "
        f"{user}@{ip}:~/{client_project_path}/"
    )
    if transfer_appname:
        os.system(f'''sshpass -p '{password}' ssh {user}@{ip} "mkdir -p ~/{client_project_path}/apps''')
        os.system(
            f"sshpass -p '{password}' scp -r {transfer_appname} {user}@{ip}:~/{client_project_path}/apps/{transfer_appname}")
    if not os.popen(
            f'''sshpass -p "{password}" ssh {user}@{ip} "cd ~/{client_project_path}/ && ls env_ok_{filename}"'''
    ).read().strip():
        os.system(
            f"sshpass -p '{password}' ssh {user}@{ip} "
            f'"cd ~/{client_project_path}/ && '
            f'bash env.sh -p {password} && touch env_ok_{filename}"'
        )


def _start_client_service(ip, password, user, filename):
    _cmd = (
        f"nohup sshpass -p '{password}' ssh {user}@{ip} "
        f'"cd ~/{client_project_path}/src/remotectl/ && '
        f'pipenv run python {filename}" > /tmp/{filename}.log 2>&1 &'
    )
    print(Fore.GREEN, _cmd, Fore.RESET)
    p = multiprocessing.Process(target=_feeling_good, args=(_cmd,))
    p.start()
    time.sleep(1)


def check_rpc_started(filename):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            user = kwargs.get('user') or args[0]
            ip = kwargs.get('ip') or args[1]
            if not user or not ip:
                raise ValueError("user and ip are required")
            password = kwargs.get('password') or (args[2] if len(args) >= 3 else conf.PASSWORD)
            transfer_app = kwargs.get('transfer_appname')
            tool_status = os.popen(
                f'''sshpass -p '{password}' ssh {user}@{ip} "ps -aux |  grep {filename} | grep -v grep"'''
            ).read()
            if not tool_status:
                _base_env_check(password)
                _transfer_to_client(ip, password, user, filename, transfer_app)
                _start_client_service(ip, password, user, filename)

            return func(*args, **kwargs)

        return wrapper

    return deco
