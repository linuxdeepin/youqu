#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
# pylint: disable=C0301,W1514,R1721,R1710,W1514,C0103,R1710
import os
import csv

from src import logger


class ReadCsv:
    """
    读取 csv 文件
    """

    __author__ = "Mikigo <huangmingqiang@uniontech.com>"

    @staticmethod
    def read_csv(csv_path):
        """
         通过标准库 csv 读取文件
        :param csv_path: 文件路径
        :return: 数据列表
        """
        if os.path.exists(csv_path):
            with open(csv_path, newline="") as csvfile:
                reader = csv.reader(csvfile)
                return [row for row in reader][1:]
        logger.error(f"{csv_path} is not exists!")

    @staticmethod
    def read_csv_by_str(csv_path, maxsplit=-1):
        """
         通过字符串处理读取字符串
        :param csv_path: 文件路径
        :param maxsplit: 最大分割次数
        :return: 数据列表
        """
        if os.path.exists(csv_path):
            with open(csv_path, "r") as f:
                txt_list = f.readlines()
            return [txt.strip().split(",", maxsplit=maxsplit) for txt in txt_list[1:]]
        logger.error(f"{csv_path} is not exists!")
