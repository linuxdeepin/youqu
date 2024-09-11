#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114,C0103
import re
from typing import Union

from setting.globalconfig import GlobalConfig
from src import logger
from src.cmdctl import CmdCtl
from src.custom_exception import ElementNotFound
from src.custom_exception import ApplicationStartError

try:
    from src.depends.dogtail.tree import SearchError
    from src.depends.dogtail.tree import root
    from src.depends.dogtail.tree import predicate
    from src.depends.dogtail.tree import config
    from src.depends.dogtail.tree import Node

    config.childrenLimit = 1000
    # config.logDebugToStdOut = False
    config.logDebugToFile = False
    config.searchCutoffCount = 2
    GlobalConfig.NO_DOGTAIL = False
except ModuleNotFoundError:
    GlobalConfig.NO_DOGTAIL = True

from src.mouse_key import MouseKey


class DogtailUtils(MouseKey):
    """
    通过属性进行元素定位和操作。
    """

    # pylint: disable=too-many-arguments,too-many-locals,too-many-public-methods
    __author__ = "Mikigo <huangmingqiang@uniontech.com>, Litao <litaoa@uniontech.com>"

    def __init__(self, name=None, description=None, number=-1, check_start=True, key: dict = None):
        if GlobalConfig.NO_DOGTAIL:
            raise EnvironmentError("Dogtail 及其相关依赖存在问题,调用相关方法失败~")
        config.logDebugToStdOut = False
        self.name = name
        self.description = description
        try:
            if name:
                self.obj = root.application(self.name, self.description)
            else:
                self.obj = root
            if number > 0:
                self.obj = self.obj.findChildren(predicate.GenericPredicate(**key))[number]

        except SearchError:
            if check_start:
                search_app = CmdCtl.run_cmd(f"ps -ef | grep {self.name}")
                logger.error(search_app)
                raise ApplicationStartError(self.name) from SearchError

    def app_element(self, *args, **kwargs) -> Node:
        """
         获取app元素的对象
        :return: 元素的对象
        """
        try:
            element = self.obj.child(*args, **kwargs, retry=False)
            logger.debug(f"{args, kwargs} 获取元素对象 <{element}>")
            return element
        except SearchError:
            raise ElementNotFound(*args, **kwargs) from SearchError

    def get_element_children_text(self, element):
        element = self.app_element(element)
        all_children = element.children
        text = []
        for i in range(len(all_children)):
            text.append(all_children[i].name)
        return text

    def left_upper_corner_position(self, element) -> tuple:
        """
         获取元素左上角的坐标
        :param element: 元素名称
        :return: 元素左上角坐标
        """
        position = self.app_element(element).position
        logger.debug(f"获取元素 {element}元素左上角坐标 {position}")
        return position

    def element_size(self, *args, **kwargs) -> tuple:
        """
         获取元素的大小
        :return: 元素大小
        """
        size = self.app_element(*args, **kwargs).size
        logger.debug(f"元素{args, kwargs} 的大小 {size}")
        return size

    def right_upper_corner_position(self, element) -> tuple:
        """
         获取元素右上角的坐标
        :param element: 元素名称
        :return: 元素右上角坐标
        """
        _x = self.left_upper_corner_position(element)[0] + self.element_size(element)[0]
        _y = self.left_upper_corner_position(element)[1]
        logger.debug(f"获取元素 {element}, 右上角坐标 ({_x, _y})")
        return int(_x), int(_y)

    def element_center(self, element) -> tuple:
        """
         获取元素的中心位置
        :param element:
        :return: 元素中心坐标
        """
        _x, _y, _w, _h = self.app_element(element).extents
        _x = _x + _w / 2
        _y = _y + _h / 2
        logger.debug(f"获取元素中心坐标 ({_x, _y})")
        return _x, _y

    def element_click(self, element, button=1):
        """
         元素点击
        :param element: 应用的元素
        :param button: 1>left,2>middle,3>right
        :return: None
        """
        logger.debug(
            f"""{"左键" if button == 1 else f"{'右键' if button == 3 else '鼠标中健'}"} 点击元素 {element}"""
        )
        mouse_click = (
            self.click if button == 1 else self.right_click if button == 3 else self.middle_click
        )
        mouse_click(*self.element_center(element))

    def element_double_click(self, element):
        """
         元素双击
        :return: None
        """
        logger.debug(f"双击元素 {element}")
        self.double_click(*self.element_center(element))

    def element_point(self, element):
        """
         鼠标移动到元素上（位置是在元素的中心）
        :param element: 应用的元素
        :return: None
        """
        logger.debug(f"鼠标移至元素 {element} 中心")
        self.move_to(*self.element_center(element))

    @staticmethod
    def __evalx(expr, element, recursive):
        """evalx"""
        node = re.match(".*?[^\\\\]/", expr)
        if node:
            name = node.group().replace("\\/", "/")[:-1]
        else:
            return False
        if name == "*":
            element = element.children
        else:
            element = element.findChildren(predicate.GenericPredicate(name), recursive=recursive)
        return node, element

    def __trace(self, element, result, expr):
        if expr.startswith("//"):
            name = expr[2:]
            node, element = self.__evalx(name, element, recursive=True)
        elif expr.startswith("/"):
            name = expr[1:]
            node, element = self.__evalx(name, element, recursive=False)
        else:
            return False
        try:
            next_node = name[node.end() - 1:]
            if next_node != "/":
                for i in element:
                    self.__trace(i, result, next_node)
            else:
                result += element
        except SearchError:
            raise ElementNotFound(expr) from SearchError
        return result

    def find_elements_by_attr(self, expr) -> Union[list, bool]:
        """
         通过层级获取元素
        :param expr: 元素定位 $/xx.xxx//xxx,  $根节点  /当前子节点， //递归查找子节点
        :return: 元素对象
        """
        logger.debug(f"查找元素 expr={expr}")
        if expr == "$":
            return self.obj if isinstance(self.obj, list) else [self.obj]
        if not expr.startswith("$"):
            return False
        if not expr.endswith("/") or expr.endswith(r"\/"):
            expr = expr + "/"
        result = self.__trace(self.obj, [], expr[1:])
        logger.debug(f"元素 {result}")
        return result

    def find_element_by_attr(self, expr, index=0) -> Node:
        """
         查找界面元素
        :param expr: 匹配格式 元素定位 $/xxx//xxx,  $根节点  /当前子节点， //递归查找子节点
        :param index: 匹配结果索引
        :return: 元素对象
        """
        elements = self.find_elements_by_attr(expr)
        if not elements:
            raise ElementNotFound(expr)
        try:
            return elements[index]
        except IndexError:
            raise ElementNotFound(f"{expr}, index:{index}") from IndexError

    def find_element_by_attr_and_click(self, expr, index=0):
        self.find_element_by_attr(expr, index).click()

    def find_element_by_attr_and_right_click(self, expr, index=0):
        self.find_element_by_attr(expr, index).click(3)

    def find_elements_to_the_end(self, ele_name):
        """
         递归查找应用界面的元素(适用于查找多个同名称元素)
        :param ele_name: 需要查找的元素名称
        :return: 查找到的元素对象的列表
        """
        eles = []
        root_ele = self.obj

        def recur_inter(node=None):
            if not node:
                node = root_ele
            children = node.children
            if children:
                for i in children:
                    if i.combovalue == ele_name:
                        eles.append(i)
                    recur_inter(i)

        recur_inter()
        return eles
