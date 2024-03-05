#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import os
from setting import conf


def sslclone(
        url: str = None,
        user: str = None,
        password: str = None,
        branch: str = None,
        depth: [str, int] = None,
        **kwargs
):
    os.system(
        f"cd {conf.ROOT_DIR}/src/utils && "
        f"bash sslclone.sh {conf.APPS_PATH} {url} {user} {password} {branch if branch else ''} {depth if depth else ''}"
    )


def clone(
        url: str = None,
        branch: str = "",
        depth: [str, int] = "",
        **kwargs
):
    os.system(
        f"cd {conf.APPS_PATH} && git clone {url} "
        f"{f'-b {branch}' if branch else ''} {f'--depth {depth}' if depth else ''}"
    )
