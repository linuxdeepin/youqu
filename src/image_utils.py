#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
# pylint: disable=E0401,C0413,R0903,W0707,W0611
try:
    import cv2 as cv

    GET_OPENCV_FORM_RPC = False
except ModuleNotFoundError:
    GET_OPENCV_FORM_RPC = True

from image_center import ImageCenter
from image_center.conf import setting as image_setting

from setting import conf

image_setting.PORT = conf.OPENCV_PORT
image_setting.SERVER_IP = conf.OPENCV_SERVER_HOST
image_setting.NETWORK_RETRY = int(conf.OPENCV_NETWORK_RETRY)
image_setting.PAUSE = float(conf.OPENCV_PAUSE)
image_setting.TIMEOUT = float(conf.OPENCV_TIMEOUT)
image_setting.MAX_MATCH_NUMBER = int(conf.OPENCV_MAX_MATCH_NUMBER)


class ImageUtils(ImageCenter):
    """图像识别的工具类"""

    # 移除此方法
    # @staticmethod
    # def opencv_compare_images_SSIM(
    #         module_name, imageA_name, imageB_name, ssim=None, app_name=None
    # ):
    #     """
    #     判断两张图片是否相同
    #     (临时解决安全中心需要外部依赖的问题，基础框架提供对应的接口;)
    #     :param module_name:模块
    #     :param imageA_name:预存图片A
    #     :param imageB_name:比较图片B
    #     example:opencv_compare_images_SSIM('system_check', 'system_check_315116', 'pms_315116')
    #     """
    #     # pylint: disable=invalid-name,I1101,E1101
    #     if ssim is None:
    #         ssim = GlobalConfig.IMAGE_RATE
    #     picture_path = f"{GlobalConfig.APPS_PATH}/{app_name}/res/picture"
    #     contrast_path = f"/home/{GlobalConfig.USERNAME}/Pictures/{app_name}"
    #     file_a = cv.imread(f"{picture_path}/{module_name}/{imageA_name}.png")
    #     file_b = cv.imread(f"{contrast_path}/{module_name}/{imageB_name}.png")
    #     file_a = cv.cvtColor(file_a, cv.COLOR_BGR2GRAY)
    #     file_b = cv.cvtColor(file_b, cv.COLOR_BGR2GRAY)
    #     result = cv.matchTemplate(file_b, file_a, cv.TM_CCOEFF_NORMED)
    #     similarity = cv.minMaxLoc(result)[1]
    #     logger.info("SSIM = " + str(similarity))
    #     if similarity >= ssim:
    #         return True
    #     return False
