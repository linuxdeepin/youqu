#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
# pylint: disable=C0301,C0103,R0904
from time import sleep
from src.mouse_key import MouseKey
from src import log


@log
class ShortCut(MouseKey):
    """快捷键"""

    @classmethod
    def ctrl_f9(cls):
        """
         ctrl_f9 快捷键设置壁纸
        :return:
        """
        cls.hot_key("ctrl", "f9")

    @classmethod
    def super_up(cls):
        """
         super_up 最大化窗口
        :return:
        """
        cls.hot_key("win", "up")

    @classmethod
    def win_left(cls):
        """
        win_left  向左切换工作区
        :return:
        """
        cls.hot_key("win", "left")

    @classmethod
    def win_right(cls):
        """
         win_right 向右切换工作区
        :return:
        """
        cls.hot_key("win", "Right")

    @classmethod
    def ctrl_shift_shortcut_down(cls):
        """
         ctrl shift ? 唤起快捷键面板
        :return:
        """
        cls.hot_key_down("ctrl", "shift", "/")

    @classmethod
    def ctrl_shift_shortcut_up(cls):
        """
         ctrl shift ? 收起快捷键面板
        :return:
        """
        cls.hot_key_up("ctrl", "shift", "/")

    @classmethod
    def shift(cls):
        """
         shift
        :return:
        """
        cls.hot_key("shift")

    @classmethod
    def shift_right(cls):
        """
         'shift' + 'right'
        :return:
        """
        cls.hot_key("shift", "right")

    @classmethod
    def shift_down(cls):
        """
         shift_down
        :return:
        """
        cls.hot_key("shift", "down")

    @classmethod
    def shift_up(cls):
        """
         shift_up
        :return:
        """
        cls.hot_key("shift", "up")

    @classmethod
    def tab(cls):
        """
         tab
        :return:
        """
        cls.press_key("tab")

    @classmethod
    def esc(cls):
        """
         esc
        :return:
        """
        cls.press_key("esc")

    @classmethod
    def right(cls):
        """
         right 键盘方向键-右键
        :return:
        """
        cls.press_key("right")

    @classmethod
    def left(cls):
        """
         left 键盘方向键-左键
        :return:
        """
        cls.press_key("left")

    @classmethod
    def dot(cls):
        """
         dot 键盘点号
        :return:
        """
        cls.press_key(".")

    @classmethod
    def press_left_sometime(cls, sometime: int):
        """
         按住键盘方向键-左键一段时间
        :param sometime: 一段时间
        :return:
        """
        cls.press_key_down("left")
        sleep(sometime)
        cls.press_key_up("left")

    @classmethod
    def up(cls):
        """
         up 键盘方向键-上键
        :return:
        """
        cls.press_key("up")

    @classmethod
    def press_up_sometime(cls, sometime: int):
        """
         按住键盘方向键-上键一段时间
        :param sometime: 一段时间
        :return:
        """
        cls.press_key_down("up")
        sleep(sometime)
        cls.press_key_up("up")

    @classmethod
    def down(cls):
        """
         down 键盘方向键-下键
        :return:
        """
        cls.press_key("down")

    @classmethod
    def enter(cls):
        """
         enter 回车
        :return:
        """
        cls.press_key("enter")

    @classmethod
    def ctrl_a(cls):
        """
         ctrl_a
        :return:
        """
        cls.hot_key("ctrl", "a")

    @classmethod
    def ctrl_l(cls):
        """
         ctrl_l
        :return:
        """
        cls.hot_key("ctrl", "l")

    @classmethod
    def ctrl_g(cls):
        """
         ctrl_g
        :return:
        """
        cls.hot_key("ctrl", "g")

    @classmethod
    def ctrl_n(cls):
        """
         ctrl_n
        :return:
        """
        cls.hot_key("ctrl", "n")

    @classmethod
    def ctrl_alt_t(cls):
        """
         ctrl_alt_t
        :return:
        """
        cls.hot_key("ctrl", "alt", "t")

    @classmethod
    def ctrl_alt_down(cls):
        """
         ctrl_alt_down
        :return:
        """
        cls.hot_key("ctrl", "alt", "down")

    @classmethod
    def ctrl_alt_up(cls):
        """
         ctrl_alt_up
        :return:
        """
        cls.hot_key("ctrl", "alt", "up")

    @classmethod
    def ctrl_alt_a(cls):
        """
         ctrl_alt_a
        :return:
        """
        cls.hot_key("ctrl", "alt", "a")

    @classmethod
    def ctrl_x(cls):
        """
         ctrl_x
        :return:
        """
        cls.hot_key("ctrl", "x")

    @classmethod
    def ctrl_s(cls):
        """
         ctrl_a
        :return:
        """
        cls.hot_key("ctrl", "s")

    @classmethod
    def alt_tab(cls):
        """
         快捷键alt+table
        :return:
        """
        cls.hot_key("alt", "tab")

    @classmethod
    def ctrl_tab(cls):
        """
         快捷键ctrl+table
        :return:
        """
        cls.hot_key("ctrl", "tab")

    @classmethod
    def ctrl_shift_tab(cls):
        """
         快捷键ctrl+table
        :return:
        """
        cls.hot_key("ctrl", "shift", "tab")

    @classmethod
    def alt_m(cls):
        """
         ctrl_m
        :return:
        """
        cls.hot_key("alt", "m")

    @classmethod
    def ctrl_f(cls):
        """
         ctrl_f
        :return:
        """
        cls.hot_key("ctrl", "f")

    @classmethod
    def ctrl_v(cls):
        """
         ctrl_v
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "v")

    @classmethod
    def ctrl_c(cls):
        """
         ctrl_c
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "c")

    @classmethod
    def alt_f4(cls):
        """
         alt_f4
        :return:
        """
        sleep(1)
        cls.hot_key("alt", "f4")

    @classmethod
    def alt_f2(cls):
        """
         alt_f2
        :return:
        """
        sleep(1)
        cls.hot_key("alt", "f2")

    @classmethod
    def f2(cls):
        """
         f2
        :return:
        """
        sleep(1)
        cls.press_key("f2")

    @classmethod
    def f1(cls):
        """
         f1
        :return:
        """
        sleep(1)
        cls.press_key("f1")

    @classmethod
    def f3(cls):
        """
         f3
        :return:
        """
        sleep(1)
        cls.press_key("f3")

    @classmethod
    def f5(cls):
        """
         f5
        :return:
        """
        sleep(1)
        cls.press_key("f5")

    @classmethod
    def space(cls):
        """
         space
        :return:
        """
        sleep(1)
        cls.press_key("space")

    @classmethod
    def backspace(cls):
        """
         backspace
        :return:
        """
        sleep(1)
        cls.press_key("backspace")

    @classmethod
    def winleft_d(cls):
        """
         winleft_d
        :return:
        """
        sleep(1)
        cls.hot_key("winleft", "d")

    @classmethod
    def winleft_q(cls):
        """
         winleft_q
        :return:
        """
        sleep(1)
        cls.hot_key("winleft", "q")

    @classmethod
    def ctrl_z(cls):
        """
         ctrl_z
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "z")
        sleep(0.5)

    @classmethod
    def ctrl_y(cls):
        """
         ctrl_y
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "y")
        sleep(0.5)

    @classmethod
    def winleft_e(cls):
        """
         winleft_e
        :return:
        """
        sleep(1)
        cls.hot_key("winleft", "e")

    @classmethod
    def delete(cls):
        """
         delete
        :return:
        """
        cls.press_key("delete")

    @classmethod
    def shift_delete(cls):
        """
         shift_delete
        :return:
        """
        cls.hot_key("shift", "delete")

    @classmethod
    def shift_left(cls):
        """
         shift+左方向键
        :return:
        """
        cls.hot_key("shift", "left")

    @classmethod
    def ctrl_i(cls):
        """
         ctrl i
        :return:
        """
        cls.hot_key("ctrl", "i")

    @classmethod
    def ctrl_h(cls):
        """
         ctrl h
        :return:
        """
        cls.hot_key("ctrl", "h")

    @classmethod
    def ctrl_o(cls):
        """
         ctrl_o
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "o")

    @classmethod
    def ctrl_shift_up(cls):
        """
         ctrl_shift_up
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "shift", "up")

    @classmethod
    def ctrl_shift_n(cls):
        """
         ctrl_shift_n
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "shift", "n")

    @classmethod
    def ctrl_shift_down(cls):
        """
         ctrl_shift_down
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "shift", "down")

    @classmethod
    def ctrl_shift_left(cls):
        """
         ctrl_shift_left
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "shift", "left")

    @classmethod
    def ctrl_shift_right(cls):
        """
         ctrl_shift_right
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "shift", "right")

    @classmethod
    def ctrl_up(cls):
        """
         ctrl_up
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "up")

    @classmethod
    def ctrl_down(cls):
        """
         ctrl_down
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "down")

    @classmethod
    def ctrl_left(cls):
        """
         ctrl_left
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "left")

    @classmethod
    def ctrl_right(cls):
        """
         ctrl_right
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "right")

    @classmethod
    def shift_space(cls):
        """
         shift+space
        :return:
        """
        sleep(1)
        cls.hot_key("shift", "space")

    @classmethod
    def ctrl_rod(cls):
        """
         ctrl+-
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "-")

    @classmethod
    def ctrl_add(cls):
        """
         ctrl++
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "+")

    @classmethod
    def ctrl_r(cls):
        """
         ctrl+r
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "r")

    @classmethod
    def ctrl_shift_r(cls):
        """
         ctrl+shift+r
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "shift", "r")

    @classmethod
    def ctrl_shift_z(cls):
        """
         ctrl+shift+z
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "shift", "z")

    @classmethod
    def ctrl_scroll(cls, direction, amount_of_scroll=1):
        """
         ctrl+滚轮
        :param direction:
        :param amount_of_scroll:
        :return:
        """
        cls.press_key_down("ctrl")
        for _ in range(amount_of_scroll):
            cls.mouse_scroll(direction, duration=0)
        cls.press_key_up("ctrl")

    @classmethod
    def shift_scroll(cls, direction, amount_of_scroll=1):
        """
         shift+滚轮
        :param direction:
        :param amount_of_scroll:
        :return:
        """
        cls.press_key_down("shift")
        for _ in range(amount_of_scroll):
            cls.mouse_scroll(direction, duration=0)
        cls.press_key_up("shift")

    @classmethod
    def alt_d(cls):
        """
         alt+d
        :return:
        """
        sleep(1)
        cls.hot_key("alt", "d")

    @classmethod
    def ctrl_e(cls):
        """
         ctrl+e
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "e")

    @classmethod
    def ctrl_shift_s(cls):
        """
         ctrl+shift+s
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "shift", "s")

    @classmethod
    def ctrl_shift(cls):
        """
         ctrl+shift
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "shift")

    @classmethod
    def ctrl_space(cls):
        """
         ctrl+space
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "space")

    @classmethod
    def ctrl_shift_e(cls):
        """
         ctrl+shift+e
        :return:
        """
        cls.hot_key("ctrl", "shift", "e")

    @classmethod
    def ctrl_shift_w(cls):
        """
         ctrl+shift+w
        :return:
        """
        cls.hot_key("ctrl", "shift", "w")

    @classmethod
    def ctrl_alt_v(cls):
        """
         快捷键打开剪切板
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "alt", "v")

    @classmethod
    def ctrl_alt_delete(cls):
        """
         快捷键打开剪切板
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "alt", "delete")

    @classmethod
    def ctrl_printscreen(cls):
        """
         快捷键启动延时截图
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "printscreen")

    @classmethod
    def alt_enter(cls):
        """
         快捷键影院进入全屏
        :return:
        """
        sleep(1)
        cls.hot_key("alt", "enter")

    @classmethod
    def printscreen(cls):
        """
         快捷键截取全屏
        :return:
        """
        sleep(1)
        cls.hot_key("printscreen")

    @classmethod
    def alt_o(cls):
        """
         ocr应用内部快捷键
        :return:
        """
        sleep(1)
        cls.hot_key("alt", "o")

    @classmethod
    def alt_s(cls):
        """
         快捷键连拍截图
        :return:
        """
        sleep(1)
        cls.hot_key("alt", "s")

    @classmethod
    def alt_p(cls):
        """
         贴图应用内部快捷键
        :return:
        """
        sleep(1)
        cls.hot_key("alt", "p")

    @classmethod
    def p(cls):
        """
         按下p快捷键
        :return:
        """
        sleep(1)
        cls.press_key("p")

    @classmethod
    def h(cls):
        """
         按下h快捷键
        :return:
        """
        sleep(1)
        cls.press_key("h")

    @classmethod
    def f(cls):
        """
         按下f快捷键
        :return:
        """
        sleep(1)
        cls.press_key("f")

    @classmethod
    def s(cls):
        """
         按下s快捷键
        :return:
        """
        sleep(1)
        cls.press_key("s")

    @classmethod
    def o(cls):
        """
         按下o快捷键
        :return:
        """
        sleep(1)
        cls.press_key("o")

    @classmethod
    def r(cls):
        """
         按下r快捷键
        :return:
        """
        sleep(1)
        cls.press_key("r")

    @classmethod
    def i(cls):
        """
         按下i快捷键
        :return:
        """
        sleep(1)
        cls.press_key("i")

    @classmethod
    def alt_shift_tab(cls):
        """
         快捷键切换应用窗口
        :return:
        """
        cls.hot_key("alt", "shift", "tab")

    @classmethod
    def alt_printscreen(cls):
        """
         快捷键 <alt + PrintScreen>
        :return:
        """
        cls.hot_key("alt", "PrintScreen")

    @classmethod
    def super_d(cls):
        """快捷键 super + d
        :return:
        """
        cls.hot_key("win", "d")

    @classmethod
    def super_l(cls):
        """快捷键 super + l
        :return:
        """
        cls.hot_key("win", "l")

    @classmethod
    def super(cls):
        """快捷键 super
        :return:
        """
        cls.hot_key("win")

    @classmethod
    def pageup(cls):
        """
         上一页
        :return:
        """
        cls.press_key("pageup")

    @classmethod
    def pagedown(cls):
        """
         下一页
        :return:
        """
        cls.press_key("pagedown")
