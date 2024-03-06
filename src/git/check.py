#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import os
from setting import conf


def check_git_installed():
    if not os.popen("git --version").read().startswith("git version"):
        print("git 没有安装，我们将尝试安装")
        os.system(f"echo '{conf.PASSWORD}' | sudo -S apt install git -y")
