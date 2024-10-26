#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only

import functools
import inspect
import multiprocessing
import os
import subprocess
import sys
import time
from os.path import dirname
from socketserver import ThreadingMixIn
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer

sys.path.append(dirname(dirname(dirname(os.path.abspath(__file__)))))

from setting import conf
# from src.depends.colorama import Fore

client_project_path = "/".join(conf.ROOT_DIR.split("/")[3:])
exclude_files = [
    "apps",
    "report",
    "public",
    "__pycache__",
    "node_modules",
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


def _base_env_check():
    sudo = f"echo '{conf.PASSWORD}' | sudo -S"
    os.system("rm -rf ~/.ssh/known_hosts")
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


def _ssh(ip, password, user):
    return f"sshpass -p '{password}' ssh {user}@{ip}"


def _transfer_appname(ip, password, user, transfer_appname):
    os.system(
        f"sshpass -p '{password}' rsync -av -e ssh --exclude='__pycache__' "
        f"{conf.APPS_PATH}/{transfer_appname} {user}@{ip}:~/{client_project_path}/apps/"
    )


def _transfer_to_client(ip, password, user):
    os.system(f'''{_ssh(ip, password, user)} "mkdir -p ~/{client_project_path}" > /dev/null 2>&1''')
    os.system(
        f"sshpass -p '{password}' rsync -av -e ssh {_exclude()} {conf.ROOT_DIR}/* "
        f"{user}@{ip}:~/{client_project_path}/"
    )
    os.system(
        f'''{_ssh(ip, password, user)} "cd ~/{client_project_path}/ && mkdir apps && touch apps/__init__.py" > /dev/null 2>&1'''
    )
    os.system(
        f'''{_ssh(ip, password, user)} "cd ~/{client_project_path}/apps/ && touch REMOTE" > /dev/null 2>&1'''
    )
    if (
            not os.popen(
                f'''{_ssh(ip, password, user)} "cd ~/{client_project_path}/ && ls env_ok"'''
            ).read().strip()
    ):
        os.system(
            f'{_ssh(ip, password, user)} "cd ~/{client_project_path}/ && bash env.sh -p {password} && touch env_ok"'
        )


def _start_client_service(ip, password, user, filename):
    if not os.path.exists(f"{conf.REPORT_PATH}/logs/"):
        os.makedirs(f"{conf.REPORT_PATH}/logs/")
    _cmd = (
        f"nohup {_ssh(ip, password, user)} "
        f'"cd ~/{client_project_path}/src/remotectl/ && '
        f'pipenv run python {filename}" >>  {conf.REPORT_PATH}/logs/{filename}.log 2>&1 &'
    )
    # print(Fore.GREEN, _cmd, Fore.RESET)
    p = multiprocessing.Process(target=_feeling_good, args=(_cmd,))
    p.start()
    time.sleep(1)


def _restart_client_service(ip, password, user, filename):
    GREP_LIST = (
        "grep",
    )
    cmd = ""
    for i in GREP_LIST:
        cmd += f"grep -v {i} | "
    os.system(
        f"{_ssh(ip, password, user)} "
        f'''"ps -ef | grep {filename} | {cmd}cut -c 9-15 | xargs kill -9 > /dev/null 2>&1"'''
    )
    time.sleep(1)
    _start_client_service(ip, password, user, filename)


def check_rpc_started(filename):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get("user") or args[0]
            ip = kwargs.get("ip") or args[1]
            if not user or not ip:
                raise ValueError("user and ip are required")
            password = kwargs.get("password") or (args[2] if len(args) >= 3 else conf.PASSWORD)
            transfer_appname = kwargs.get("transfer_appname")
            restart_service = kwargs.get("restart_service")

            _base_env_check()
            if transfer_appname:
                _transfer_appname(ip, password, user, transfer_appname)
            tool_status = os.popen(
                f'''{_ssh(ip, password, user)} "ps -aux |  grep {filename} | grep -v grep"'''
            ).read()
            if not tool_status:
                _transfer_to_client(ip, password, user)
                _start_client_service(ip, password, user, filename)
            if restart_service:
                _restart_client_service(ip, password, user, filename)
            res = func(*args, **kwargs)

            return res

        return wrapper

    return deco


def remote_client(ip, port):
    try:
        import zerorpc
    except ImportError:
        raise ImportError("Please install zerorpc")

    c = zerorpc.Client(timeout=20, heartbeat=None)
    try:
        c.connect(f"tcp://{ip}:{port}")
        return c
    except Exception as e:
        raise e
    finally:
        c.close()


def remote_server(obj, port):
    try:
        import zerorpc
    except ImportError:
        raise ImportError("Please install zerorpc")
    server = zerorpc.Server(obj)
    server.bind(f"tcp://0.0.0.0:{port}")
    server.run()


class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer): ...


def _remote_client(ip, port):
    client = ServerProxy(f"http://{ip}:{port}", allow_none=True)
    return client


def _remote_server(obj, port):
    server = ThreadXMLRPCServer(("0.0.0.0", port), allow_none=True)
    for func, _ in inspect.getmembers(obj):
        if not func.startswith("_"):
            server.register_function(getattr(obj, func), func)
    server.serve_forever()


if __name__ == '__main__':
    from src import Src

    _remote_server(Src(), 4242)
