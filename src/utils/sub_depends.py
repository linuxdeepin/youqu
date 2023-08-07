#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
import os

for root, dirs, files in os.walk(os.path.abspath("../../apps")):
    for file in files:
        if file == "requirement.txt":
            print(f"{root}/{file}")
