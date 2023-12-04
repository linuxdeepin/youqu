#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
# pylint: disable=R0913,C0413,E0401
import sys

from funnylog import log
from funnylog import logger

from setting.globalconfig import SystemPath

for i in SystemPath:
    if i.value not in sys.path:
        sys.path.append(i.value)

from src.dbus_utils import DbusUtils
from src.assert_common import AssertCommon
from src.calculate import Calculate
from src.cmdctl import CmdCtl
from src.dogtail_utils import DogtailUtils
from src.image_utils import ImageUtils
from src.ocr_utils import OCRUtils as OCR
from src.button_center import ButtonCenter
from src.filectl import FileCtl
from src.shortcut import ShortCut
from src.mouse_key import MouseKey
from src.custom_exception import *
from src.sleepx import sleep
from src.video_utils import VideoUtils
from src.read_csv import ReadCsv
from src.pinyin import pinyin


class Src(
    CmdCtl,
    ImageUtils,
    FileCtl,
    ShortCut,
    Calculate,
    OCR,
):
    """src"""

    def __init__(
            self,
            name=None,
            description=None,
            config_path=None,
            number=-1,
            check_start=True,
            ui_name=None,
            **kwargs,
    ):
        """dogtail or button center param
        :param kwargs: app_name, desc, number
        """
        self.dog = DogtailUtils(
            name=name,
            description=description,
            number=number,
            check_start=check_start,
            **kwargs,
        )
        ui_name = ui_name if ui_name else name
        # pylint: disable=invalid-name
        self.ui = ButtonCenter(app_name=ui_name, config_path=config_path, number=number)
