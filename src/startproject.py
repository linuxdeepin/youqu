#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
import sys
import os
from configparser import ConfigParser
from configparser import NoSectionError


def cli():
    """Command Line Create Project"""
    args = sys.argv[1:]
    project_name = "youqu"
    root_dir = os.path.dirname(os.path.abspath(__file__))
    if len(args) == 1:
        project_name = args[0]
    elif len(args) > 1:
        raise ValueError("只能接受 1 个参数")

    if os.path.exists(f"./{project_name}"):
        raise FileExistsError(f"目录:{project_name} 已经存在，请确认您要创建的项目名称！")
    os.system(f"rm -rf /tmp/{project_name}")
    os.makedirs(f"/tmp/{project_name}")
    os.system(f"cp -r {root_dir}/. /tmp/{project_name}/")
    os.system(f"mv /tmp/{project_name} .")
    os.system(f"rm -rf {project_name}/startproject.py")
    os.system(f"rm -rf {project_name}/.gitignore")
    for root, dirs, files in os.walk(f"./{project_name}"):
        for d in dirs:
            if d == "__pycache__":
                os.system(f"rm -rf {root}/{d}")
    conf = ConfigParser()
    try:
        conf.read(f"{root_dir}/CURRENT")
        youqu_version = conf.get("current", "tag")
    except NoSectionError:
        youqu_version = None
    print(
        f"The project: [\033[0;32m{project_name}\033[0m],has been created by youqu{f'-{youqu_version}' if youqu_version else ''}"
    )


if __name__ == "__main__":
    cli()
