#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
import os
from time import sleep

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


class WindowState(ctypes.Structure):
    """window structure"""

    _fields_ = [
        ("pid", ctypes.c_int),  # 4
        ("windowId", ctypes.c_int),  # 4
        ("resourceName", ctypes.c_char * 256),  # 256
        ("Geometry", Geometry),  # 16
        ("isMinimized", ctypes.c_bool),  # 4
        ("isFullScreen", ctypes.c_bool),
        ("isActive", ctypes.c_bool),
        ("splitable", ctypes.c_int),  # 4
        ("uuid", ctypes.c_char * 256),  # 256
    ]


class dtk_array(ctypes.Structure):
    _fields_ = [
        ("size", ctypes.c_size_t),
        ("alloc", ctypes.c_size_t),
        ("data", ctypes.POINTER(WindowState)),
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


class WaylandWindowInfo:
    """获取窗口信息"""

    def __init__(self):
        self.library = ctypes.cdll.LoadLibrary(f"/usr/lib/{machine()}-linux-gnu/libdtkwmjack.so")
        if not GlobalConfig.DTK_DISPLAY:
            self.init_dtk_display()
            GlobalConfig.DTK_DISPLAY = True

    def init_dtk_display(self):
        self.library.InitDtkWmDisplay()

    def destory_dtk_display(self):
        self.library.DestoryDtkWmDisplay()

    def _window_info(self):
        """窗口信息"""
        self.library.GetWindowFromPoint.restype = ctypes.c_int
        wid = self.library.GetWindowFromPoint()
        self.library.GetWindowState.restype = ctypes.POINTER(WindowStructure)
        ws = self.library.GetWindowState(wid)
        window_info = ws.contents.Geometry
        resourceName = ws.contents.resourceName.decode("utf-8")
        if not resourceName:
            resourceName = os.popen(f"cat /proc/{ws.contents.pid}/cmdline").read().strip("\x00")
        return {
            "name": resourceName,
            "wininfo": (window_info.x, window_info.y, window_info.width, window_info.height),
        }

    def window_info(self):
        """窗口信息"""
        self.library.GetAllWindowStatesList.restype = ctypes.c_int
        _e = None
        for _ in range(3):
            try:
                windows_pointer = ctypes.pointer(WindowState())
                range_index = self.library.GetAllWindowStatesList(ctypes.byref(windows_pointer))
                break
            except ValueError as e:
                _e = e
                sleep(1)
        else:
            raise ValueError(_e)
        res = {}
        for i in range(int(range_index)):
            window_info = windows_pointer[i]
            resource_name = window_info.resourceName.decode("utf-8")
            if " " in resource_name:
                _resource_name_1, _resource_name_2 = resource_name.split(" ")
                resource_name = _resource_name_1 or _resource_name_2
            _info = {
                "location": (
                    window_info.Geometry.x,
                    window_info.Geometry.y,
                    window_info.Geometry.width,
                    window_info.Geometry.height,
                ),
                "pid": window_info.pid,
                "window_id": window_info.windowId,
                "uuid": window_info.uuid.decode("utf-8"),
                "is_minimized": window_info.isMinimized,
                "is_full_screen": window_info.isFullScreen,
                "is_active": window_info.isActive,
            }
            if res.get(resource_name) is None:
                res[resource_name] = _info
            else:
                if isinstance(res.get(resource_name), dict):
                    res[resource_name] = [res.get(resource_name), _info]
                elif isinstance(res.get(resource_name), list):
                    res[resource_name].append(_info)
        return res


if __name__ == "__main__":
    wwininfo = WaylandWindowInfo()
    wwininfo.window_info()
    # wwininfo.library.InitDtkWmDisplay()
    # for i in range(100):
    #     print(wwininfo.window_info())
    #     sleep(1)
    # wwininfo.library.DestoryDtkWmDisplay()
