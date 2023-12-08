#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
import os

from setting.globalconfig import GlobalConfig
# wayland PATH
if GlobalConfig.IS_WAYLAND:
    os.environ["QT_WAYLAND_SHELL_INTEGRATION"] = "kwayland-shell"
    os.environ["XDG_SESSION_DESKTOP"] = "Wayland"
    os.environ["XDG_SESSION_TYPE"] = "wayland"
    os.environ["WAYLAND_DISPLAY"] = "wayland-0"
    os.environ["GDMSESSION"] = "Wayland"
    os.environ["DBUS_SESSION_BUS_ADDRESS"] = "unix:path=/run/user/1000/bus"

from platform import machine
import ctypes


class Geometry(ctypes.Structure):
    """sub structure"""
    _fields_ = [
        ("x", ctypes.c_int),
        ("y", ctypes.c_int),
        ("width", ctypes.c_int),
        ("height", ctypes.c_int),
    ]


class WindowStructure(ctypes.Structure):
    """window structure"""
    _fields_ = [
        ("pid", ctypes.c_int),
        ("windowId", ctypes.c_int),
        ("resourceName", ctypes.c_char * 256),
        ("Geometry", Geometry),
        ("isMinimized", ctypes.c_bool),
        ("isFullScreen", ctypes.c_bool),
        ("isActive", ctypes.c_bool),
    ]


class WaylandWindowINfo:
    """获取窗口信息"""

    def __init__(self):
        self.library = ctypes.cdll.LoadLibrary(f"/usr/lib/{machine()}-linux-gnu/libdtkwmjack.so")
        self.library.InitDtkWmDisplay()

    def window_id(self):
        """窗口id"""
        self.library.GetWindowFromPoint.restype = ctypes.c_int
        wid = self.library.GetWindowFromPoint()
        return wid

    def window_info(self):
        """窗口信息"""
        wid = self.window_id()
        self.library.GetWindowState.restype = ctypes.POINTER(WindowStructure)
        ws = self.library.GetWindowState(wid)
        window_info = ws.contents.Geometry
        resourceName = ws.contents.resourceName.decode("utf-8")
        if not resourceName:
            resourceName = os.popen(f"cat /proc/{ws.contents.pid}/cmdline").read().strip()
        return {
            "name": resourceName,
            "wininfo": (
                window_info.x,
                window_info.y,
                window_info.width,
                window_info.height
            ),
        }

if __name__ == '__main__':
    WaylandWindowINfo().window_info()