#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
import os

py_debs = []
for root, dirs, files in os.walk(os.path.abspath("../../apps")):
    for file in files:
        if file == "requirement_deb.txt":
            with open(f"{root}/{file}", "r", encoding="utf-8") as f:
                py_debs.extend([i.strip() for i in f.read().split("\n")])

print(" ".join(py_debs), end="")
