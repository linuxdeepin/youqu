#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
# pylint: disable=R0913,C0413,E0401
import sys

from funnylog import log as log
from funnylog import logger as logger
from funnylog.conf import setting as log_setting
from setting.globalconfig import GlobalConfig

log_setting.LOG_FILE_PATH = GlobalConfig.REPORT_PATH

from setting.globalconfig import SystemPath

for i in SystemPath:
    if i.value not in sys.path:
        sys.path.append(i.value)

from src.dbus_utils import DbusUtils as DbusUtils
from src.assert_common import AssertCommon as AssertCommon
from src.calculate import Calculate as Calculate
from src.cmdctl import CmdCtl as CmdCtl
from src.dogtail_utils import DogtailUtils as DogtailUtils
from src.image_utils import ImageUtils as ImageUtils
from src.ocr_utils import OCRUtils as OCR
from src.button_center import ButtonCenter as ButtonCenter
from src.filectl import FileCtl as FileCtl
from src.shortcut import ShortCut as ShortCut
from src.mouse_key import MouseKey as MouseKey
from src.video_utils import VideoUtils as VideoUtils
from src.read_csv import ReadCsv as ReadCsv
from src.pinyin import pinyin as pinyin
from src.sleepx import sleep as sleep
from src.custom_exception import *


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
