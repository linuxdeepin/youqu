#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
import os

LOOP_STOP = False
for root, dirs, files in os.walk(os.path.abspath("../../apps")):
    for file in files:
        if file == "BASICENV":
            print("BASICENV", end="")
            LOOP_STOP = True
            break
    if LOOP_STOP:
        break
