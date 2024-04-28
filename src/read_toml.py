#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import tomli


def read_toml(file_path):
    with open(file_path, "rb") as config_file:
        toml_dict = tomli.load(config_file)
    return toml_dict


if __name__ == "__main__":
    from setting import conf

    read_toml(f"{conf.ROOT_DIR}/playbook.toml")
