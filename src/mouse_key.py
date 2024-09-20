#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only

import os
import sys
from time import sleep

from src import logger
from src.cmdctl import CmdCtl

os.environ["DISPLAY"] = ":0"

from setting.globalconfig import GlobalConfig


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


with HiddenPrints():
    if GlobalConfig.IS_WAYLAND:
        # pylint: disable=ungrouped-imports

        from src.depends.pyautogui import _pyautogui_wayland as pyautogui
        from src.depends.pyautogui._pyautogui_wayland import popen
    else:
        from src.depends import pyautogui

pyautogui.FAILSAFE = False


# pyautogui.PAUSE = 1


class MouseKey:
    """
    鼠标和键盘的常用操作
    """

    __author__ = "Mikigo <huangmingqiang@uniontech.com>, Litao <litaoa@uniontech.com>"

    MOUSE = {1: pyautogui.PRIMARY, 2: pyautogui.MIDDLE, 3: pyautogui.RIGHT}

    @classmethod
    def screen_size(cls):
        """
         获取屏幕大小
        :return: width, height
        """
        width, height = pyautogui.size()
        logger.debug(f"获取屏幕分辨率 {width}*{height}")
        return width, height

    @classmethod
    def current_location(cls, out_log=True):
        """
         获取当前鼠标位置
        :return: 鼠标当前的坐标
        """
        position = pyautogui.position()
        if out_log:
            logger.debug(f"当前鼠标坐标 {position}")
        return position

    @classmethod
    def move_to(cls, _x, _y, duration=0.4):
        """
         移动到指定位置
        :param _x: x
        :param _y: y
        :param duration:移动的速度
        :return:
        """
        logger.debug(f"鼠标移动至 ({_x, _y}, 速度：{duration})")
        pyautogui.moveTo(int(_x), int(_y), duration=duration)

    @classmethod
    def move_rel(cls, _x, _y, duration=0.4):
        """
         相对移动到位置
        :param _x:
        :param _y:
        :param duration:
        :return:
        """
        logger.debug(f"鼠标移动相对坐标位置 ({_x, _y}), 速度：{duration}")
        pyautogui.moveRel(xOffset=int(_x), yOffset=int(_y), duration=duration)

    @classmethod
    def click(cls, _x=None, _y=None, _type="pyautogui"):
        """
         点击鼠标左键
        :param _x:
        :param _y:
        :param _type: 使用 PyAutoGUI or Xdotool 点击
        :return:
        """
        logger.debug(f"点击坐标 {(_x, _y) if _x else cls.current_location(out_log=False)}")
        if _type == "pyautogui":
            pyautogui.click(x=_x, y=_y)
        else:
            if GlobalConfig.IS_WAYLAND:
                pyautogui.click(x=_x, y=_y)
            else:
                CmdCtl.run_cmd(f"xdotool mousemove {_x} {_y} click 1")

    @classmethod
    def move_rel_and_click(cls, _x, _y):
        """
         move relative and click
        :param _x:
        :param _y:
        :return:
        """
        cls.move_rel(_x, _y)
        cls.click()

    @classmethod
    def middle_click(cls):
        """
        单击鼠标滚轮中间
        """
        logger.debug("单击鼠标滚轮中间")
        pyautogui.middleClick()

    @classmethod
    def right_click(cls, _x=None, _y=None):
        """
         单击鼠标右键
        :param _x:
        :param _y:
        :return:
        """
        logger.debug(f"鼠标右键坐标 {(_x, _y) if _x else cls.current_location(out_log=False)}")
        pyautogui.rightClick(x=_x, y=_y)
        sleep(1)

    @classmethod
    def double_click(cls, _x=None, _y=None, interval=0.3):
        """
         双击鼠标左键
        :param _x:
        :param _y:
        :param interval: 两次点击的间隔，默认 0.3s
        :return:
        """
        logger.debug(f"鼠标左键双击坐标 {(_x, _y) if _x else cls.current_location(out_log=False)}")
        pyautogui.doubleClick(x=_x, y=_y, interval=interval)
        # CmdCtl.run_cmd(f"xdotool mousemove {_x} {_y} click --repeat 2 1")
        sleep(1)

    @classmethod
    def triple_click(cls, _x=None, _y=None):
        """
         三击鼠标左键
        :param _x:
        :param _y:
        :return:
        """
        logger.debug(f"鼠标三连击坐标 {(_x, _y) if _x else cls.current_location(out_log=False)}")
        pyautogui.tripleClick(x=_x, y=_y, interval=0.3)
        sleep(1)

    @classmethod
    def drag_to(cls, _x, _y, duration=0.4, delay=1):
        """
         拖拽到指定位置(绝对位置)
        :param _x: 拖拽到的位置x
        :param _y: 拖拽到的位置y
        :param duration: 拖拽的时长
        :param delay: 拖拽后等待的时间
        :return:
        """
        logger.debug(f"鼠标从当前位置拖拽到坐标 ({_x, _y})")
        # 默认duration=0.4时，拖拽到_y<=95不生效，将拖拽的时长调整为0.9，
        # 至于为啥_y<=95且duration<=0.8 时不生效，目前还不清楚，先解决问题
        if _y <= 95:
            duration = 0.9
        pyautogui.dragTo(x=int(_x), y=int(_y), duration=duration, mouseDownUp=True)
        sleep(delay)

    @classmethod
    def drag_rel(cls, _x, _y):
        """
         按住鼠标左键,拖拽到指定位置(相对位置)
        :param _x: 拖拽的相对位置x，正数向右，负数向左
        :param _y: 拖拽的相对位置y，正数向下，负数向上
        :return:
        """
        logger.debug(f"鼠标从当前位置拖拽到相对坐标 ({_x, _y})")
        pyautogui.dragRel(xOffset=int(_x), yOffset=int(_y), duration=0.4, mouseDownUp=True)
        sleep(1)

    @classmethod
    def mouse_down(cls, _x=None, _y=None, button=1):
        """
         按住鼠标键不放
        :param _x:
        :param _y:
        :param button: 1 左键， 2 中键， 3 右键
        :return:
        """
        logger.debug(
            f"在坐标 {(_x, _y) if _x else cls.current_location(out_log=False)} "
            f"处按住鼠标{['左', '中', '右'][button - 1]}键不放"
        )
        pyautogui.mouseDown(x=_x, y=_y, button=cls.MOUSE.get(button, pyautogui.PRIMARY))

    @classmethod
    def mouse_up(cls, button=1):
        """
         松开鼠标左键
        :param button: 1 左键， 2 中键， 3 右键
        :return:
        """
        logger.debug(f"松开鼠标{['左', '中', '右'][button - 1]}键")
        pyautogui.mouseUp(button=cls.MOUSE.get(button, pyautogui.PRIMARY))
        sleep(1)

    @classmethod
    def mouse_scroll(cls, amount_of_scroll, duration=1):
        """
         滚动鼠标滚轮,the_amount_of_scroll为传入滚轮数,正数为向上,负数为向下
        :param amount_of_scroll: 滚轮数
        :param duration:
        :return:
        """
        pyautogui.scroll(amount_of_scroll)
        if amount_of_scroll > 0:
            direct = "上"
        else:
            direct = "下"
        logger.debug(f"向<{direct}>滑动滚轮")
        sleep(duration)

    @classmethod
    def input_message(
            cls,
            message,
            delay_time: int = 300,
            interval: [int, float] = 0.2,
            wayland_shift: bool = False,
            _ydotool: bool = False,
    ):
        """
         输入字符串
        :param message: 输入的内容
        :param delay_time: 延迟时间
        :param interval:
        :return:
        """
        logger.debug(f"输入字符串<{message}>")
        message = str(message)

        def check_chinese():
            for _ch in message:
                if "\u4e00" <= _ch <= "\u9fff":
                    return True
            return False

        if GlobalConfig.IS_X11:
            if check_chinese():
                CmdCtl.run_cmd(f"xdotool type --delay {delay_time} '{message}'", timeout=60)
            else:
                pyautogui.typewrite(message=str(message), interval=interval)
        # wayland上
        else:
            if check_chinese():
                # 复制
                os.system(f"wl-copy \"{message}\"")
                # 有些地方可能不支持ctrl+v粘贴，比如终端，需要使用ctrl+shift+v
                _hk = ["ctrl", "v"]
                if wayland_shift:
                    _hk.insert(1, "shift")
                cls.hot_key(*_hk)
            else:
                for key in message:
                    if _ydotool:
                        from src import ydotool

                        ydotool.press(key)
                    else:
                        pyautogui.press(key, interval=interval)

    @classmethod
    def press_key(cls, key: str, interval=0.0, _ydotool: bool = False):
        """
         键盘上指定的按键
        :param key: 键盘按键
        :param interval:
        :return:
        """
        logger.debug(f"点击键盘上指定的按键<{key}>, 间隔<{interval}>")
        if _ydotool:
            from src import ydotool

            ydotool.press(key)
        else:
            pyautogui.press(key, interval=interval)

    @classmethod
    def press_key_down(cls, key: str):
        """
         按住键盘按键不放
        :param key: 键盘按键
        :return:
        """
        logger.debug(f"按下<{key}>按键")
        pyautogui.keyDown(key)

    @classmethod
    def press_key_up(cls, key: str):
        """
         放松按键
        :param key: 键盘按键
        :return:
        """
        logger.debug(f"放松<{key}>按键")
        pyautogui.keyUp(key)

    @classmethod
    def hot_key(cls, *args, interval=0.03):
        """
         键盘组合按键操作
        :param args: 键盘组合键，比如："ctrl","alt","a"
        :return:
        """
        logger.debug(f"快捷键 {args}")
        pyautogui.hotkey(*args, interval=interval)

    @classmethod
    def hot_key_down(cls, *args):
        """
         组合按键按下不放
        :param args:
        :return:
        """
        for _c in args:
            if len(_c) > 1:
                _c = _c.lower()
            cls.press_key_down(_c)
            sleep(0.03)

    @classmethod
    def hot_key_up(cls, *args):
        """
         组合按键释放
        :param args:
        :return:
        """
        for c in reversed(args):
            if len(c) > 1:
                c = c.lower()
            cls.press_key_up(c)
            sleep(0.03)

    @classmethod
    def move_to_and_click(cls, _x, _y):
        """
         移动到某个位置点击
        :param _x: 移动到的位置 x
        :param _y: 移动到的位置 y
        :return:
        """
        cls.move_to(_x, _y)
        cls.click()

    @classmethod
    def move_to_and_right_click(cls, _x, _y):
        """
         移动到某个位置点击右键
        :param _x: 移动到的位置 x
        :param _y: 移动到的位置 y
        :return:
        """
        cls.move_to(_x, _y)
        cls.right_click()

    @classmethod
    def move_to_and_double_click(cls, _x, _y):
        """
         移动到某个位置点击双击
        :param _x: 移动到的位置 x
        :param _y: 移动到的位置 y
        :return:
        """
        cls.move_to(_x, _y)
        cls.double_click()

    @classmethod
    def move_on_and_drag_to(cls, start: tuple, end: tuple):
        """
         指定拖动的起始-终止坐标
        :param start: 开始坐标
        :param end: 终止坐标
        :return:
        """
        cls.move_to(*start)
        sleep(1)
        cls.drag_to(*end)

    @classmethod
    def move_on_and_drag_rel(cls, start: tuple, end: tuple):
        """
         指定拖动的起始-终止坐标
        :param start: 开始坐标
        :param end: 终止坐标
        :return:
        """
        cls.move_to(*start)
        sleep(1)
        cls.drag_rel(*end)

    @classmethod
    def select_menu(cls, number: int):
        """
         选择桌面右键菜单中的选项(从上到下)
        :param number: 在菜单中的位置数
        :return:
        """
        for _ in range(number):
            cls.press_key("down")
        sleep(0.3)
        cls.press_key("enter")
        logger.debug(f"选择右键菜单中的选项(从上到下)第{number}项")

    @classmethod
    def reverse_select_menu(cls, number: int):
        """
         选择桌面右键菜单中的选项（从下到上）
        :param number: 在菜单中的位置数
        :return:
        """
        for _ in range(number):
            cls.press_key("up")
        sleep(0.3)
        cls.press_key("enter")
        logger.debug(f"选择右键菜单中的选项(从下到上)第{number}项")

    @classmethod
    def select_submenu(cls, number: int):
        """
         选择右键菜单中的子菜单选项（从上到下）
        :param number: 在菜单中的位置数
        :return:
        """
        for _ in range(1, number):
            cls.press_key("down")
        cls.press_key("enter")

    @classmethod
    def locate_all_on_screen(cls, image_path):
        """
         识别所有匹配的图像
        :param image_path: 图像的路径
        :return: 所有匹配的位置的元组组成的列表
        """
        return pyautogui.locateAllOnScreen(image_path)

    @classmethod
    def draw_line(cls, start_x, start_y, rel_x, rel_y):
        """
         从某个坐标开始画线（框选）
        :param start_x: 开始的坐标的横坐标
        :param start_y: 开始的坐标的纵坐标
        :param rel_x: 向量的横坐标
        :param rel_y: 向量的纵坐标
        :return:
        """
        cls.move_to(start_x, start_y)
        cls.drag_rel(rel_x, rel_y)

    @classmethod
    def clear(cls):
        """
         清空表单
        :return:
        """
        logger.debug("清空表单")
        cls.hot_key("ctrl", "a")
        cls.press_key("backspace")
