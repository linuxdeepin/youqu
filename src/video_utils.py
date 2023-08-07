#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114,E1101
try:
    import cv2
except ModuleNotFoundError:
    pass


class VideoUtils:
    """
    获取视频属性的方法
    """

    @staticmethod
    def video_fps(path):
        """
         视频的帧率
        :param path: 视频路径
        :return:
        """
        cap = cv2.VideoCapture(path)
        return cap.get(cv2.CAP_PROP_FPS)

    @staticmethod
    def resolution(path):
        """
         视频的分辨率
        :param path: 视频路径
        :return:
        """
        cap = cv2.VideoCapture(path)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        return width, height

    @staticmethod
    def video_time(path):
        """
         视频的时长
        :param path: 视频路径
        :return:
        """
        cap = cv2.VideoCapture(path)
        fps_ = cap.get(cv2.CAP_PROP_FPS)
        frame_number = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        return frame_number / fps_
