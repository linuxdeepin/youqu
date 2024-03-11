#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import os
from setting import conf

def git_config():
    os.system("git config --global http.lowSpeedLimit 0")
    os.system("git config --global http.lowSpeedTime 999999")

def sslclone(
        url: str = None,
        user: str = None,
        password: str = None,
        branch: str = None,
        depth: [str, int] = None,
        **kwargs,
):
    branch = branch or conf.BRANCH
    depth = depth or conf.DEPTH
    git_config()
    os.system(
        f"cd {conf.ROOT_DIR}/src/utils && "
        f"bash sslclone.sh {conf.APPS_PATH} "
        f"{url or conf.GIT_URL} "
        f"{user or conf.GTI_USER} {password or conf.GIT_PASSWORD} "
        f"{branch or ''} {depth or ''}"
    )


def clone(
        url: str = None,
        branch: str = "",
        depth: [str, int] = "",
        **kwargs
):
    branch = branch or conf.BRANCH
    depth = depth or conf.DEPTH
    git_config()
    os.system(
        f"cd {conf.APPS_PATH} && git clone {url} "
        f"{url or conf.GIT_URL}"
        f"{f'-b {branch}' or ''} {f'--depth {depth}' or ''}"
    )
