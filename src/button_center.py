#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only

import re
from configparser import ConfigParser, NoSectionError
from time import sleep

import dbus

from setting.globalconfig import GlobalConfig
from src import logger
from src.cmdctl import CmdCtl
from src.custom_exception import ApplicationStartError
from src.custom_exception import GetWindowInformation
from src.custom_exception import NoSetReferencePoint
from src.shortcut import ShortCut
from src.wayland_wininfo import WaylandWindowInfo


class ButtonCenter:
    """
    根据应用程序中控件元素的相对坐标，通过配置元素的x、y、w和h来定位元素在屏幕中的位置，并返回用于鼠标和键盘操作的坐标。
    """

    __author__ = "Mikigo <huangmingqiang@uniontech.com>, Litao <litaoa@uniontech.com>"

    def __init__(
        self, app_name: str, config_path: str, number: int = -1, pause: int = 1, retry: int = 1
    ):
        """
        :param app_name: 系统应用软件包，例如，dde-file-manager
        :param config_path: ui 定位配置文件路径（绝对路径）
        :param number: 默认为 -1, 即最后一个窗口
            如果你想指定不同的窗口，你可以在实例化对象的时候显式的传入 number，第一个为 0
        """
        self.app_name = app_name
        self.number = number
        # 每个操作步骤之前暂停的时间
        self.pause = pause
        self.config_path = config_path
        self.retry = retry

    def window_info(self):
        """
         窗口信息
        :return:  窗口的基本信息，左上角坐标，窗口宽高等
        """
        if GlobalConfig.IS_X11:
            try:
                # Get window_operate ID based on package name
                app_id = (
                    CmdCtl.run_cmd(
                        f"xdotool search --classname --onlyvisible {self.app_name}",
                        interrupt=False,
                        out_debug_flag=False,
                        command_log=False,
                    )
                    .strip()
                    .split("\n")
                )
                app_id_list = [int(_id) for _id in app_id if _id]
                app_id_list.sort()
                logger.debug(f"app_id_list: {app_id_list}")
                return CmdCtl.run_cmd(
                    f"xwininfo -id {app_id_list[self.number]}",
                    interrupt=False,
                    out_debug_flag=False,
                    command_log=False,
                )
            except Exception as exc:
                raise ApplicationStartError(f"{self.app_name, exc}") from exc

        elif GlobalConfig.IS_WAYLAND:
            self.wwininfo = WaylandWindowInfo()
            if hasattr(self.wwininfo.library, "GetAllWindowStatesList"):
                for _ in range(self.retry + 1):
                    info = self.wwininfo.window_info().get(self.app_name)
                    if info is None:
                        sleep(1)
                    else:
                        break
                else:
                    raise ApplicationStartError(self.app_name)
                if isinstance(info, dict):
                    return info
                elif isinstance(info, list):
                    return info[self.number]
            else:
                proxy_object = dbus.SessionBus().get_object("org.kde.KWin", "/dde")
                dbus.Interface(proxy_object, "org.kde.KWin").WindowMove()
                sleep(self.pause)
                ShortCut.esc()
                return self.wwininfo._window_info()
        return None

    def window_location_and_sizes(self):
        """
         获取窗口的位置及大小
        :return:
        """
        try:
            if GlobalConfig.IS_X11:
                for _ in range(self.retry + 1):
                    app_window_info = self.window_info()
                    re_pattern = re.compile(r"Absolute.*:\s\s(-?\d+)")
                    result = re.findall(re_pattern, app_window_info)
                    if not result:
                        sleep(1)
                    else:
                        break
                else:
                    raise ApplicationStartError(self.app_name)
                window_width = re.findall(r"Width.*:\s(\d+)", app_window_info)[0]
                window_height = re.findall(r"Height.*:\s(\d+)", app_window_info)[0]
                window_x, window_y = result
            else:
                self.wwininfo = WaylandWindowInfo()
                if hasattr(self.wwininfo.library, "GetAllWindowStatesList"):
                    app_window_info = self.window_info()
                    window_x, window_y, window_width, window_height = app_window_info.get(
                        "location"
                    )
                else:
                    app_window_info = self.window_info()
                    name = app_window_info.get("name")
                    if name != self.app_name:
                        raise ValueError(
                            f"您想要获取的窗口为：{self.app_name}, 但实际获取的窗口为：{name}"
                        )
                    window_x, window_y, window_width, window_height = app_window_info.get("wininfo")
            logger.debug(
                f"窗口左上角坐标 {window_x, window_y},获取窗口大小 {window_width}*{window_height}"
            )
            return (int(window_x), int(window_y), int(window_width), int(window_height))
        except (IndexError, KeyError) as exc:
            raise GetWindowInformation(f"获取窗口大小错误 {exc}") from exc

    def window_left_top_position(self) -> tuple:
        """
         获取窗口左上角坐标
        :return:  (0, 0)
        """
        try:
            re_pattern = re.compile(r"Absolute.*:\s\s(-?\d+)")
            app_window_info = self.window_info()
            if GlobalConfig.IS_X11:
                result = re.findall(re_pattern, app_window_info)
                if not result:
                    sleep(1)
                    result = re.findall(re_pattern, self.window_info())
                window_x, window_y = result
            else:
                self.wwininfo = WaylandWindowInfo()
                if hasattr(self.wwininfo.library, "GetAllWindowStatesList"):
                    window_x, window_y, window_width, window_height = app_window_info.get(
                        "location"
                    )
                else:
                    window_x, window_y, window_width, window_height = app_window_info.get("wininfo")
            logger.debug(f"窗口左上角坐标 {window_x, window_y}")
            return int(window_x), int(window_y)
        except (ValueError, KeyError) as exc:
            raise GetWindowInformation(f"获取窗口左上角坐标错误 {exc}") from exc

    def window_sizes(self) -> tuple:
        """
         获取窗口的大小
        :return:  (宽， 高)， 例如：(400, 600)
        """
        try:
            app_window_info = self.window_info()
            if GlobalConfig.IS_X11:
                window_width = re.findall(r"Width.*:\s(\d+)", app_window_info)[0]
                window_height = re.findall(r"Height.*:\s(\d+)", app_window_info)[0]
            else:
                self.wwininfo = WaylandWindowInfo()
                if hasattr(self.wwininfo.library, "GetAllWindowStatesList"):
                    window_x, window_y, window_width, window_height = app_window_info.get(
                        "location"
                    )
                else:
                    window_x, window_y, window_width, window_height = app_window_info.get("wininfo")
            logger.debug(f"获取窗口大小 {window_width}*{window_height}")
            return int(window_width), int(window_height)
        except (IndexError, KeyError) as exc:
            raise GetWindowInformation(f"获取窗口大小错误 {exc}") from exc

    def window_left_bottom_position(self) -> tuple:
        """
         左下角的坐标
        :return:  (0, 1080)
        """
        (
            window_x,
            window_y,
            _window_width,
            window_height,
        ) = self.window_location_and_sizes()
        left_y = window_y + window_height
        logger.debug(f"窗口左下角坐标 {window_x, left_y}")
        return int(window_x), int(left_y)

    def window_right_top_position(self) -> tuple:
        """
         右上角的坐标
        :return:  (1920, 0)
        """
        (
            window_x,
            window_y,
            window_width,
            _window_height,
        ) = self.window_location_and_sizes()
        right_x = window_x + window_width
        logger.debug(f"窗口右上角坐标 {right_x, window_y}")
        return int(right_x), int(window_y)

    def window_right_bottom_position(self) -> tuple:
        """
         右下角的坐标
        :return:  (1920, 1080)
        """
        (
            window_x,
            window_y,
            window_width,
            window_height,
        ) = self.window_location_and_sizes()
        right_x = window_x + window_width
        right_y = window_y + window_height
        logger.debug(f"窗口右下角坐标 {right_x, right_y}")
        return int(right_x), int(right_y)

    def window_left_center_position(self) -> tuple:
        """
         获取窗口左边界中心坐标
        :return:  (0, 540)
        """
        (
            window_x,
            window_y,
            _window_width,
            window_height,
        ) = self.window_location_and_sizes()
        center_y = window_y + window_height / 2
        logger.debug(f"窗口左边界中心坐标 {window_x, center_y}")
        return int(window_x), int(center_y)

    def window_top_center_position(self) -> tuple:
        """
         获取窗口上边界中心坐标
        :return:  (960, 0)
        """
        (
            window_x,
            window_y,
            window_width,
            _window_height,
        ) = self.window_location_and_sizes()
        center_x = window_x + window_width / 2
        logger.debug(f"获取窗口上边界中心坐标 {center_x, window_y}")
        return int(center_x), int(window_y)

    def window_right_center_position(self) -> tuple:
        """
         获取窗口右边界中心坐标
        :return:  (1920, 540)
        """
        (
            window_x,
            window_y,
            window_width,
            window_height,
        ) = self.window_location_and_sizes()
        right_x = window_x + window_width
        center_y = window_y + window_height / 2
        logger.debug(f"获取窗口右边界中心坐标 {right_x, center_y}")
        return int(right_x), int(center_y)

    def window_bottom_center_position(self) -> tuple:
        """
         获取窗口下边界中心的坐标
        :return:  (960, 1080)
        """
        (
            window_x,
            window_y,
            window_width,
            window_height,
        ) = self.window_location_and_sizes()
        center_x = window_x + window_width / 2
        bottom_y = window_y + window_height
        logger.debug(f"获取窗口下边界中心的坐标 {center_x, bottom_y}")
        return int(center_x), int(bottom_y)

    def window_center(self) -> tuple:
        """
         获取窗口的中心点坐标
        :return:  (960, 540)
        """
        (
            window_x,
            window_y,
            window_width,
            window_height,
        ) = self.window_location_and_sizes()
        _x = window_x + window_width / 2
        _y = window_y + window_height / 2
        logger.debug(f"窗口中心坐标 {_x, _y}")
        return _x, _y

    def btn_center_by_left_top(self, button_x, button_y, button_w, button_h) -> tuple:
        """
         根据左上角的坐标按钮的中心坐标
        :param button_x: 控件左上角相对于窗口左上角的横向距离
        :param button_y: 控件左上角相对于窗口左上角的纵向距离
        :param button_w: 控件宽度
        :param button_h: 控件高度
        :return:  控件的中心坐标 （1, 1）
        """
        window_x, window_y = self.window_left_top_position()
        b_x = window_x + button_x + button_w / 2
        b_y = window_y + button_y + button_h / 2
        logger.debug(f"左上角按钮的中心坐标 {b_x, b_y}")
        return b_x, b_y

    def btn_center_by_right_top(self, button_x, button_y, button_w, button_h) -> tuple:
        """
         根据右上角的坐标按钮的中心坐标
        :param button_x: 控件右上角相对于窗口右上角的横向距离
        :param button_y: 控件右上角相对于窗口右上角的纵向距离
        :param button_w: 控件宽度
        :param button_h: 控件高度
        :return:  控件的中心坐标 （1, 1）
        """
        window_x, window_y = self.window_right_top_position()
        b_x = window_x - button_x - button_w / 2
        b_y = window_y + button_y + button_h / 2
        logger.debug(f"右上角按钮的中心坐标 {b_x, b_y}")
        return b_x, b_y

    def btn_center_by_left_bottom(self, button_x, button_y, button_w, button_h) -> tuple:
        """
         根据左下角的坐标按钮的中心坐标
        :param button_x: 控件左下角相对于窗口左下角的横向距离
        :param button_y: 控件左下角相对于窗口左下角的纵向距离
        :param button_w: 控件宽度
        :param button_h: 控件高度
        :return:  控件的中心坐标 （1, 1）
        """
        window_x, window_y = self.window_left_bottom_position()
        b_x = window_x + button_x + button_w / 2
        b_y = window_y - button_y - button_h / 2
        logger.debug(f"左下角按钮的中心坐标 {b_x, b_y}")
        return b_x, b_y

    def btn_center_by_right_bottom(self, button_x, button_y, button_w, button_h) -> tuple:
        """
         根据右下角的坐标按钮的中心坐标
        :param button_x: 控件右下角相对于窗口右下角的横向距离
        :param button_y: 控件右下角相对于窗口右下角的纵向距离
        :param button_w: 控件宽度
        :param button_h: 控件高度
        :return:  控件的中心坐标 （1, 1）
        """
        window_x, window_y = self.window_right_bottom_position()
        b_x = window_x - button_x - button_w / 2
        b_y = window_y - button_y - button_h / 2
        logger.debug(f"右下角按钮的中心坐标 {b_x, b_y}")
        return b_x, b_y

    def btn_pic_by_left_top(self, button_x, button_y, button_w, button_h) -> tuple:
        """
         根据左上角的坐标按钮的截图区域
        :param button_x: 控件左上角相对于窗口左上角的横向距离
        :param button_y: 控件左上角相对于窗口左上角的纵向距离
        :param button_w: 控件宽度
        :param button_h: 控件高度
        :return:  控件的中心坐标 （1, 1）
        """
        window_x, window_y = self.window_left_top_position()
        b_x = window_x + button_x
        b_y = window_y + button_y
        logger.debug(f"左上角按钮的截取区域左上角 {b_x, b_y}, 控件长宽 {button_w, button_h}")
        return b_x, b_y, button_w, button_h

    def btn_pic_by_right_top(self, button_x, button_y, button_w, button_h) -> tuple:
        """
         根据右上角的坐标按钮的截图区域
        :param button_x: 控件右上角相对于窗口右上角的横向距离
        :param button_y: 控件右上角相对于窗口右上角的纵向距离
        :param button_w: 控件宽度
        :param button_h: 控件高度
        :return:  控件的中心坐标 （1, 1）
        """
        window_x, window_y = self.window_right_top_position()
        b_x = window_x - button_x - button_w
        b_y = window_y + button_y
        logger.debug(f"右上角按钮的截取区域左上角 {b_x, b_y}, 控件长宽 {button_w, button_h}")
        return b_x, b_y, button_w, button_h

    def btn_pic_by_left_bottom(self, button_x, button_y, button_w, button_h) -> tuple:
        """
         根据左下角的坐标按钮的截图区域
        :param button_x: 控件左下角相对于窗口左下角的横向距离
        :param button_y: 控件左下角相对于窗口左下角的纵向距离
        :param button_w: 控件宽度
        :param button_h: 控件高度
        :return:  控件的中心坐标 （1, 1）
        """
        window_x, window_y = self.window_left_bottom_position()
        b_x = window_x + button_x
        b_y = window_y - button_y - button_h
        logger.debug(f"左下角按钮的截取区域左上角 {b_x, b_y}, 控件长宽 {button_w, button_h}")
        return b_x, b_y, button_w, button_h

    def btn_pic_by_right_bottom(self, button_x, button_y, button_w, button_h) -> tuple:
        """
         根据右下角的坐标按钮的截图区域
        :param button_x: 控件右下角相对于窗口右下角的横向距离
        :param button_y: 控件右下角相对于窗口右下角的纵向距离
        :param button_w: 控件宽度
        :param button_h: 控件高度
        :return:  控件的中心坐标 （1, 1）
        """
        window_x, window_y = self.window_right_bottom_position()
        b_x = window_x - button_x - button_w
        b_y = window_y - button_y - button_h
        logger.debug(f"右下角按钮的截取区域左上角 {b_x, b_y}, 控件长宽 {button_w, button_h}")
        return b_x, b_y, button_w, button_h

    def btn_center(
        self,
        btn_name,
        offset_x=None,
        multiplier_x=None,
        offset_y=None,
        multiplier_y=None,
    ) -> tuple:
        """
         获取元素的中心坐标
        :param btn_name: 控件名
        :param offset_x
            正数为右移动
            负数为左移动
        :param multiplier_x
            offset_x 移动的倍数
        :param offset_y
            正数为上移动
            负数为下移动
        :param multiplier_y
            offset_y 移动的倍数
        """
        btn_x = btn_y = ""
        sleep(self.pause)
        conf = ConfigParser()
        if isinstance(self.config_path, list):
            for config in self.config_path:
                conf.read(config)
        elif isinstance(self.config_path, str):
            conf.read(self.config_path)
        else:
            raise ValueError
        try:
            direction = conf.get(btn_name, "direction")
        except NoSectionError:
            raise NoSectionError(f"在 [{self.config_path}] 文件中没有配置 '{btn_name}'")
        position = [int(i.strip()) for i in conf.get(btn_name, "location").split(",")]
        default_point = ("left_bottom", "left_top", "right_top", "right_bottom")
        default_boundary_point = (
            "top_center",
            "bottom_center",
            "left_center",
            "right_center",
        )
        if direction in default_point:
            btn_x, btn_y = getattr(self, f"btn_center_by_{direction}")(*position)
        elif direction in default_boundary_point:
            window_x, window_y = getattr(self, f"window_{direction}_position")()
            # pylint: disable=eval-used
            btn_x = eval(
                f"{window_x} + {position[0]} {'+' if position[0] > 0 else '-'} {position[2] / 2}"
            )
            # pylint: disable=eval-used
            btn_y = eval(
                f"{window_y} + {position[1]} {'+' if position[1] > 0 else '-'} {position[3] / 2}"
            )
        elif direction == "window_size":
            btn_x, btn_y, button_w, button_y = self.window_location_and_sizes()
            btn_x = btn_x + button_w / 2
            btn_y = btn_y + button_y / 2
        if btn_x and btn_y:
            if offset_x:
                btn_x = btn_x + int(offset_x) * (int(multiplier_x) if multiplier_x else 1)
            if offset_y:
                btn_y = btn_y + int(offset_y) * (int(multiplier_y) if multiplier_y else 1)
            logger.debug(f"[{btn_name}] 坐标：{str(btn_x)}, {str(btn_y)})")
            return btn_x, btn_y
        raise NoSetReferencePoint(
            f"{direction}, 默认参考点 {default_point + default_boundary_point}"
        )

    def btn_size(
        self,
        btn_name: str,
        offset_x: [int, float] = None,
        multiplier_x: [int, float] = None,
        offset_y: [int, float] = None,
        multiplier_y: [int, float] = None,
    ) -> tuple:
        """
         获取元素的左上角坐标及长宽
        :param btn_name: 控件名
        :param offset_x
            正数为右移动
            负数为左移动
        :param multiplier_x
            offset_x 移动的倍数
        :param offset_y
            正数为上移动
            负数为下移动
        :param multiplier_y
            offset_y 移动的倍数
        """
        btn_x = btn_y = button_w = button_y = ""
        sleep(self.pause)
        conf = ConfigParser()
        conf.read(self.config_path)
        direction = conf.get(btn_name, "direction")
        position = [int(i.strip()) for i in conf.get(btn_name, "location").split(",")]
        default_point = ("left_bottom", "left_top", "right_top", "right_bottom")
        default_boundary_point = (
            "top_center",
            "bottom_center",
            "left_center",
            "right_center",
        )
        if direction in default_point:
            btn_x, btn_y, button_w, button_y = getattr(self, f"btn_pic_by_{direction}")(*position)
        elif direction in default_boundary_point:
            window_x, window_y = getattr(self, f"window_{direction}_position")()
            btn_x = window_x + position[0] - (0 if position[0] > 0 else position[2])
            btn_y = window_y + position[1] - (0 if position[1] > 0 else position[3])
            button_w, button_y = position[2], position[3]
        elif direction == "window_size":
            btn_x, btn_y, button_w, button_y = self.window_location_and_sizes()
        if btn_x != "" and btn_y != "":
            if offset_x:
                btn_x = btn_x + int(offset_x) * (int(multiplier_x) if multiplier_x else 1)
            if offset_y:
                btn_y = btn_y + int(offset_y) * (int(multiplier_y) if multiplier_y else 1)
            logger.debug(
                f"[{btn_name}] 左上角坐标：{str(btn_x)}, {str(btn_y)}), 长宽 {button_w, button_y}"
            )
            return btn_x, btn_y, button_w, button_y
        raise NoSetReferencePoint(
            f"{direction}, 默认参考点 {default_point + default_boundary_point}"
        )

    def btn_info(self, btn_name: str) -> tuple:
        """
         元素的相对位置和参考系
        :param btn_name: 控件名称
        :return: (相对坐标，参考系）
        """
        conf = ConfigParser()
        conf.read(self.config_path)
        direction = conf.get(btn_name, "direction")
        position = [int(i.strip()) for i in conf.get(btn_name, "location").split(",")]
        return position, direction

    def get_windows_number(self, name: str) -> int:
        """
         获取应用所有窗口数量
        :param name: 应用包名
        :return: int 窗口数量
        """
        if GlobalConfig.IS_X11:
            cmd = f"xdotool search --classname --onlyvisible {name}"
            app_id = CmdCtl.run_cmd(
                cmd, interrupt=False, out_debug_flag=False, command_log=False
            ).strip()
            return len([i for i in app_id.split("\n") if i])
        else:
            info = WaylandWindowInfo().window_info().get(self.app_name)
            if isinstance(info, dict):
                return 1
            elif isinstance(info, list):
                return len(info)

    def get_windows_id(self, name: str) -> list:
        """
         获取活动应用窗口ID
        :param name: 应用包名
        :return: 窗口编号列表
        """
        if GlobalConfig.IS_X11:
            cmd = f"xdotool search --onlyvisible --classname {name}"
            app_id = CmdCtl.run_cmd(
                cmd, interrupt=False, out_debug_flag=False, command_log=False
            ).strip()
            if app_id:
                return [i for i in app_id.split("\n") if i]
            raise ApplicationStartError(app_id)
        else:
            info = self.wwininfo.window_info().get(self.app_name)
            if isinstance(info, dict):
                return info.get("window_id")
            elif isinstance(info, list):
                return [i.get("window_id") for i in info]

    def focus_windows(self, app_name: str = None):
        """
         窗口置顶并聚焦
        :param app_name: 应用包名
        """
        if GlobalConfig.IS_WAYLAND:
            return
        app_id = self.get_windows_id(app_name if app_name else self.app_name)
        windows = int(app_id[self.number])
        cmd = f"xdotool windowactivate {windows}"
        CmdCtl.run_cmd(cmd, interrupt=False, out_debug_flag=False, command_log=False)
        logger.debug(f"<{app_name}> 窗口置顶并聚焦")

    def get_lastest_window_id(self, app_name: str) -> int:
        """
         获取应用的所有窗口编号，并返回编号最大的窗口ID
        :return: 返回最新创建的窗口编号
        """
        if GlobalConfig.IS_X11:
            try:
                app_id = (
                    CmdCtl.run_cmd(
                        f"xdotool search --classname --onlyvisible {app_name}",
                        interrupt=False,
                        out_debug_flag=False,
                        command_log=False,
                    )
                    .strip()
                    .split("\n")
                )
                app_id_list = [int(_id) for _id in app_id if _id]  # to int
                app_id_list.sort()
                return app_id_list[-1]
            except Exception as exc:
                raise ApplicationStartError(f"{app_name, exc}") from exc
        else:
            info = WaylandWindowInfo().window_info().get(self.app_name)
            if isinstance(info, dict):
                return info.get("window_id")
            elif isinstance(info, list):
                return info[-1].get("window_id")
