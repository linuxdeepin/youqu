#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import os
from time import sleep
from setting import conf


def git_config():
    os.system("git config --global http.lowSpeedLimit 0")
    os.system("git config --global http.lowSpeedTime 999999")


def sslclone(
    url: str = None,
    user: str = None,
    password: str = None,
    branch: str = None,
    path_to: str = None,
    depth: [str, int] = None,
    **kwargs,
):
    branch = branch or conf.BRANCH
    depth = depth or conf.DEPTH
    if path_to is None:
        path_to = "apps"
    git_config()
    clone_cmd = (
        f"cd {conf.ROOT_DIR}/src/utils && "
        f"bash sslclone.sh {conf.ROOT_DIR}/{path_to} "
        f"{url or conf.GIT_URL} "
        f"{user or conf.GTI_USER} {password or conf.GIT_PASSWORD} "
        f"{branch or ''} {depth or ''}"
    )
    print(clone_cmd)
    os.system(clone_cmd)
    # relax
    sleep(2)


def clone(url: str = None, branch: str = "", path_to: str = None, depth: [str, int] = "", **kwargs):
    branch = branch or conf.BRANCH
    depth = depth or conf.DEPTH
    if path_to is None:
        path_to = "apps"
    git_config()
    clone_cmd = (
        f"cd {conf.ROOT_DIR}/{path_to} && git clone "
        f"{url or conf.GIT_URL} "
        f"{f'-b {branch}' if branch else ''} {f'--depth {depth}' if depth else ''}"
    )
    print(clone_cmd)
    os.system(clone_cmd)
    # relax
    sleep(2)
