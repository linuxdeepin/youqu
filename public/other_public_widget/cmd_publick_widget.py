#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
import os

import letmego

from setting.globalconfig import GlobalConfig
from src import log

@letmego.mark
@log
class CmdPublicWidget:

    def reboot(self):
        """reboot"""
        os.system(f"echo '{GlobalConfig.PASSWORD}' | sudo -S reboot")