#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import functools
import os.path
import pathlib
import shutil
import time

from youqu3 import logger
from youqu3 import setting
from youqu3.cmd import Cmd, RemoteCmd


def exclude():
    exclude_files = [
        "report",
        "__pycache__",
        ".pytest_cache",
        ".vscode",
        ".idea",
        ".git",
    ]

    exclude_str = ""
    for i in exclude_files:
        exclude_str += f"--exclude='{i}' "

    return exclude_str


def server_rootdir(project_abspath: str = None):
    path = "." if project_abspath is None else project_abspath
    return pathlib.Path(path).absolute()


def client_rootdir(user, project_abspath):
    return f"/home/{user}/_rpc_{server_rootdir(project_abspath).name}"


def transfer_to_client(ip, password, user, project_abspath):
    rsync = 'rsync -av -e "ssh -o StrictHostKeyChecking=no"'
    Cmd.run(f"rm -rf ~/.ssh/known_hosts")
    remote_cmd = RemoteCmd(user, ip, password)
    remote_cmd.remote_run(f"mkdir -p {client_rootdir(user, project_abspath)}")
    Cmd.expect_run(
        f"/bin/bash -c '{rsync} {exclude()} {server_rootdir(project_abspath)}/* {user}@{ip}:{client_rootdir(user, project_abspath)}/'",
        events={'password': f'{password}\n'},
        return_code=True
    )
    Cmd.expect_run(
        f"/bin/bash -c '{rsync} {exclude()} {server_rootdir(project_abspath)}/.env {user}@{ip}:{client_rootdir(user, project_abspath)}/'",
        events={'password': f'{password}\n'},
        return_code=True
    )
    from invoke.exceptions import UnexpectedExit
    try:
        stdout, return_code = remote_cmd.remote_run(f"cd {client_rootdir(user, project_abspath)}/ && ls env_ok",
                                                    return_code=True)
    except UnexpectedExit:
        _, return_code = remote_cmd.remote_run(
            "export PATH=$PATH:$HOME/.local/bin;"
            f"cd {client_rootdir(user, project_abspath)} && youqu3 envx && touch env_ok",
            return_code=True
        )
        logger.info(f"RPC环境安装{'成功' if return_code == 0 else '失败'} - < {user}@{ip} >")


def start_client_service(ip, password, user, filename, project_abspath):
    service_name = f"{filename}.service"
    remote_cmd = RemoteCmd(user, ip, password)
    from invoke.exceptions import UnexpectedExit
    try:
        remote_cmd.remote_run(f"ls /lib/systemd/system/{service_name}")
    except UnexpectedExit:
        remote_cmd.remote_sudo_run(
            f"cp {os.path.join(client_rootdir(user, project_abspath), service_name)} /lib/systemd/system/")
        remote_cmd.remote_sudo_run(f"chmod 644 /lib/systemd/system/{service_name}")
        remote_cmd.remote_sudo_run(f"systemctl daemon-reload")
        remote_cmd.remote_sudo_run(f"systemctl restart {service_name}")
        time.sleep(1)


def restart_client_service(ip, password, user, filename):
    RemoteCmd(user, ip, password).remote_sudo_run(f"sudo systemctl restart {filename}.service")
    time.sleep(1)


def gen_service_file(user, filename, project_abspath):
    service_file = pathlib.Path(project_abspath).absolute() / f"{filename}.service"
    service_py = setting.RPC_PATH / f"{filename}.py"
    if service_file.exists() and os.path.exists(os.path.join(project_abspath, f"{filename}.py")):
        return

    tpl_file = setting.RPC_PATH / "rpc_tpl.service"
    with open(tpl_file, "r", encoding="utf-8") as sf:
        service_tmp = sf.read()
    service_tmp.format(
        user=user,
        client_rootdir=client_rootdir(user, project_abspath),
        start_service=f"pipenv run python {filename}"
    )
    with open(service_file, "w", encoding="utf-8") as sf:
        sf.write(
            service_tmp.format(
                user=user,
                client_rootdir=client_rootdir(user, project_abspath),
                start_service=f"pipenv run python {filename}.py"
            )
        )
    shutil.copyfile(service_py, os.path.join(project_abspath, f"{filename}.py"))


def guard_rpc(filename):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get("user") or args[0]
            ip = kwargs.get("ip") or args[1]
            if not user or not ip:
                raise ValueError("user and ip are required")
            password = kwargs.get("password")
            project_abspath = kwargs.get("project_abspath")
            auto_restart = kwargs.get("auto_restart")
            return_code = None
            try:
                _, return_code = RemoteCmd(user, ip, password).remote_sudo_run(f"systemctl status {filename}.service")
            except BaseException:
                gen_service_file(user, filename, project_abspath)
                transfer_to_client(ip, password, user, project_abspath)
                start_client_service(ip, password, user, filename, project_abspath)
            if return_code != 0:
                gen_service_file(user, filename, project_abspath)
                transfer_to_client(ip, password, user, project_abspath)
                start_client_service(ip, password, user, filename, project_abspath)
            else:
                Cmd.run(f"rm -f {project_abspath}/{filename}.py")
                Cmd.run(f"rm -f {project_abspath}/{filename}.service")
            if auto_restart:
                restart_client_service(ip, password, user, filename)
            res = func(*args, **kwargs)
            return res

        return wrapper

    return deco
