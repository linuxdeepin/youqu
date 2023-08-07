# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
from os.path import join
from os.path import dirname
from os.path import abspath

from setting.globalconfig import _GlobalConfig
from setting.globalconfig import GetCfg


# pylint: disable=too-few-public-methods
class _Config(_GlobalConfig):
    """
    Application library configuration
    """

    # pylint: disable=too-few-public-methods
    class DirName:
        """DirName"""

        # pylint: disable=too-few-public-methods
        class SubDirName:
            """SubDirName"""
            UI_INI = "ui.ini"
            PIC_RES = "pic_res"

    ABSOLUTE_BASE_PATH = dirname(abspath(__file__))
    # res 目录下子目录绝对路径
    UI_INI_PATH = join(ABSOLUTE_BASE_PATH, DirName.SubDirName.UI_INI)
    PIC_RES_PATH = join(ABSOLUTE_BASE_PATH, DirName.SubDirName.PIC_RES)

    # config ini object
    CONFIG_FILE_PATH = join(ABSOLUTE_BASE_PATH, "config.ini")
    cfg = GetCfg(CONFIG_FILE_PATH, "config")

    # config.ini
    DESKTOP_CONFIG = cfg.get("DESKTOP_CONFIG")
    FTP_ADDRESS = cfg.get("FTP_ADDRESS")


Config = _Config()
