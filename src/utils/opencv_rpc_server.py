#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
# pylint: disable=too-many-locals
import math
from os.path import join
from os.path import dirname
from os.path import abspath
from os.path import exists
from os import makedirs
from time import time
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer

# pylint: disable=import-error
import pypinyin
import cv2 as cv
import numpy as np


class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    """ThreadXMLRPCServer"""


CURRENT_DIR = dirname(abspath(__file__))


def image_put(data):
    """上传图片"""
    pic_dir = join(CURRENT_DIR, "pic")
    if not exists(pic_dir):
        makedirs(pic_dir)

    pic_path = join(pic_dir, f"pic_{time()}.png")
    # pylint: disable=consider-using-with
    handle = open(pic_path, "wb")
    handle.write(data.data)
    handle.close()
    return pic_path


def pinyin(word) -> str:
    """
     汉字转化为拼音
    :param word: 待转化的汉语字符串
    :return: 拼音字符串
    """
    _s = ""
    for key in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        _s += "".join(key)
    return _s


def match_image_by_opencv(template_path, source_path, rate=None, multiple=False):
    """
     图像识别，匹配小图在屏幕中的坐标 x, y
    :param image_path: 图像识别目标文件的存放路径
    :param rate: 匹配度
    :param multiple: 是否返回匹配到的多个目标
    :return: 根据匹配度返回坐标
    """
    # pylint: disable=I1101,E1101
    template = cv.imread(template_path)
    # pylint: disable=I1101,E1101
    source = cv.imread(source_path)
    # pylint: disable=I1101,E1101
    result = cv.matchTemplate(source, template, cv.TM_CCOEFF_NORMED)
    if not multiple:
        # pylint: disable=I1101,E1101
        pos_start = cv.minMaxLoc(result)[3]
        _x = int(pos_start[0]) + int(template.shape[1] / 2)
        _y = int(pos_start[1]) + int(template.shape[0] / 2)
        # pylint: disable=I1101,E1101
        similarity = cv.minMaxLoc(result)[1]
        if similarity < rate:
            return False
        return _x, _y
    # else:
    loc = np.where(result >= rate)
    tmp_list_out = []
    tmp_list_in = []
    loc_list = list(zip(*loc))
    for i in range(0, len(loc_list) - 1):
        tmp_list_in.append(loc_list[i])
        if (
                loc_list[i + 1][0] != loc_list[i][0]
                or (loc_list[i + 1][1] - loc_list[i][1]) > 1
        ):
            tmp_list_out.append(tmp_list_in)
            tmp_list_in = []
            continue
        if i == len(loc_list) - 2:
            tmp_list_in.append(loc_list[-1])
            tmp_list_out.append(tmp_list_in)
    result_list = []
    x_list, y_list = [], []
    if tmp_list_out:
        for i in tmp_list_out:
            for j in i:
                x_list.append(j[1])
                y_list.append(j[0])
            _x = np.mean(x_list) + int(template.shape[1] / 2)
            _y = np.mean(y_list) + int(template.shape[0] / 2)
            result_list.append((_x, _y))
            x_list, y_list = [], []
        result_list.sort(key=lambda x: x[0])
        return result_list
    return False


def coordinate_distance(start: tuple, end: tuple) -> float:
    """
     计算两个坐标之间的直线距离
    :param start: 起始坐标
    :param end: 终止坐标
    :return: 两点之间距离
    """
    position_start = np.array(start)
    position_end = np.array(end)
    position_res = position_end - position_start
    return math.hypot(position_res[0], position_res[1])


def translational_coordinates(start: tuple, relative: tuple) -> np.ndarray:
    """
     计算坐标平移
    :param start: 起始坐标
    :param relative: 平移的相对坐标
    :return: 平移后的坐标
    """
    position_start = np.array(start)
    position_end = np.array(relative)
    return np.sum([position_start, position_end], axis=0)


if __name__ == "__main__":
    server = ThreadXMLRPCServer(("10.8.13.78", 8889), allow_none=True)
    server.register_function(image_put, "image_put")
    server.register_function(pinyin, "pinyin")
    server.register_function(match_image_by_opencv, "match_image_by_opencv")
    server.register_function(coordinate_distance, "coordinate_distance")
    server.register_function(translational_coordinates, "translational_coordinates")
    print("监听客户端请求。。")
    server.serve_forever()
