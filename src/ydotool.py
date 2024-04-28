#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
__author__ = "huangmingqiang@uniontech.com"

import functools
import os
from time import sleep

from setting import conf
from src import CmdCtl

KEY_NAMES = {
    " ": 57,
    "'": 40,
    "*": 55,
    "+": 78,
    ",": 51,
    "-": 12,
    ".": 52,
    "/": 53,
    "0": 11,
    "1": 2,
    "2": 3,
    "4": 5,
    "5": 6,
    "3": 4,
    "6": 7,
    "7": 8,
    "8": 9,
    "9": 10,
    ";": 39,
    "=": 13,
    "[": 26,
    "\\": 43,
    "]": 27,
    "`": 41,
    "a": 30,
    "b": 48,
    "c": 46,
    "d": 32,
    "e": 18,
    "f": 33,
    "g": 34,
    "h": 35,
    "i": 23,
    "j": 36,
    "k": 37,
    "l": 38,
    "m": 50,
    "n": 49,
    "o": 24,
    "p": 25,
    "q": 16,
    "r": 19,
    "s": 31,
    "t": 20,
    "u": 22,
    "v": 47,
    "w": 17,
    "x": 45,
    "y": 21,
    "z": 44,
    "add": 78,
    "alt": 56,
    "altleft": 56,
    "altright": 100,
    "backspace": 14,
    "capslock": 58,
    "ctrl": 29,
    "ctrlleft": 29,
    "ctrlright": 97,
    "del": 111,
    "delete": 111,
    "down": 108,
    "end": 107,
    "enter": 28,
    "esc": 1,
    "escape": 1,
    "f1": 59,
    "f10": 68,
    "f11": 87,
    "f12": 88,
    "f13": 183,
    "f14": 184,
    "f15": 185,
    "f16": 186,
    "f17": 187,
    "f18": 188,
    "f19": 189,
    "f2": 60,
    "f20": 190,
    "f21": 191,
    "f22": 192,
    "f23": 193,
    "f24": 194,
    "f3": 61,
    "f4": 62,
    "f5": 63,
    "f6": 64,
    "f7": 65,
    "f8": 66,
    "f9": 67,
    "home": 172,
    "insert": 110,
    "left": 105,
    "num0": 82,
    "num1": 79,
    "num2": 80,
    "num3": 81,
    "num4": 75,
    "num5": 76,
    "num6": 77,
    "num7": 71,
    "num8": 72,
    "num9": 73,
    "numlock": 69,
    "pagedown": 109,
    "pageup": 104,
    "pgdn": 109,
    "pgup": 104,
    "print": 210,
    "right": 106,
    "scrolllock": 70,
    "printscreen": 210,
    "shift": 42,
    "shiftleft": 42,
    "shiftright": 54,
    "space": 57,
    "tab": 15,
    "up": 103,
    "volumedown": 114,
    "volumeup": 115,
    "win": 125,
    "winleft": 125,
    "winright": 126,
    ")": 11,
    "!": 2,
    "@": 3,
    "#": 4,
    "$": 5,
    "%": 6,
    "^": 7,
    "&": 8,
    "(": 10,
    "_": 12,
    "~": 41,
    "{": 26,
    "}": 27,
    "|": 43,
    ":": 39,
    '"': 40,
    "<": 51,
    ">": 52,
    "?": 53,
    "A": 30,
    "B": 48,
    "C": 46,
    "D": 32,
    "E": 18,
    "F": 33,
    "G": 34,
    "H": 35,
    "I": 23,
    "J": 36,
    "K": 37,
    "L": 38,
    "M": 50,
    "N": 49,
    "O": 24,
    "P": 25,
    "Q": 16,
    "R": 19,
    "S": 31,
    "T": 20,
    "U": 22,
    "V": 47,
    "W": 17,
    "X": 45,
    "Y": 21,
    "Z": 44,
    "。": 52,
}


def context_manager(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        tool_status = os.popen("ps aux | grep ydotoold | grep -v grep").read()
        if not tool_status:
            os.system(
                f'echo "{conf.PASSWORD}" | sudo -S apt update;'
                f'echo "{conf.PASSWORD}" | sudo -S apt install -y scdoc;'
                f"cd {conf.ROOT_DIR}/src/depends/ydotool/;"
                "mkdir build;"
                "cd build;"
                "cmake ..;"
                'make -j "$(nproc)";'
                f'echo "{conf.PASSWORD}" | sudo -S make install'
            )
            sleep(1)
            res = os.popen(
                f'echo "{conf.PASSWORD}" | sudo -S -b '
                'ydotoold --socket-path="$HOME/.ydotool_socket" --socket-own="$(id -u):$(id -g)"'
            )
            if "未找到命令" in res:
                raise EnvironmentError("ydotool not installed")
            sleep(2)
        return func(*args, **kwargs)

    return wrapper


@context_manager
def _popen(cmd):
    return CmdCtl.run_cmd(cmd, out_debug_flag=False, command_log=False)


def press(keys):
    key_code = KEY_NAMES.get(keys)
    if key_code is None:
        raise ValueError(f"{keys} is not in KEY_NAMES")
    _popen(f'YDOTOOL_SOCKET="$HOME/.ydotool_socket" ydotool key {key_code}:1 {key_code}:0')
