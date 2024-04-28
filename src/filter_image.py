#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
from time import strftime
from os.path import splitext
from pprint import pprint

import pyscreenshot
from PIL import Image
from PIL import ImageChops

from setting.globalconfig import GlobalConfig
from src.mouse_key import MouseKey

right_action = (
    MouseKey.click,
    MouseKey.right_click,
    MouseKey.double_click,
    MouseKey.move_to,
)


def filter_image(action):
    """
    对比动作前后两张图片，提取不同的部分生成一张新的图片，并返回新图片的路径
    :param action: 动作函数的函数对象
    :return: 新图片的路径
    """
    if not hasattr(action, "__call__"):
        print(f"{action} 不是一个函数对象")
        raise ValueError

    if action not in right_action:
        pprint(f"{action.__name__} 不在 {[i.__name__ for i in right_action]}")
        raise ValueError

    before_img_path = splitext(GlobalConfig.SCREEN_CACHE)[0] + "_before.png"
    pyscreenshot.grab().save(before_img_path)
    before_img = Image.open(before_img_path)
    action()
    after_img_path = splitext(GlobalConfig.SCREEN_CACHE)[0] + "_after.png"
    pyscreenshot.grab().save(after_img_path)
    after_img = Image.open(after_img_path)

    filter_img = ImageChops.difference(before_img, after_img)
    if filter_img.getbbox() is None:
        print(f"{before_img_path}、{after_img_path}两张图片相同")
        return None
    res_img = splitext(GlobalConfig.SCREEN_CACHE)[0] + f'_{strftime("%Y%m%d%H%M%S")}.png'
    filter_img.save(res_img)
    return res_img


if __name__ == "__main__":
    filter_image(MouseKey.right_click)
