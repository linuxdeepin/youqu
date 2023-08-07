#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
import os
import sys

for root, dirs, files in os.walk(os.path.abspath("../../apps")):
    for file in files:
        if file == "sources.list":
            print(f"{root}/{file}", end="")
            sys.exit(0)
