#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114

import dbus


class DbusUtils:
    """
    Obtain or operate the DBUS interface of the application through DBUS
    """

    def __init__(self, dbus_name=None, object_path=None, interface=None):
        """
        You can view the following parameters through d-feet.
        dbus_name
            eg.com.deepin.daemon.Appearance
        object_path
            eg./com/deepin/daemon/Appearance
        interface
            eg.com.deepin.daemon.Appearance

        Install d-feet using the command 'sudo apt install d-feet'
        """
        self.dbus_name = dbus_name
        self.object_path = object_path
        self.interface = interface
        self.session_dbus = dbus.SessionBus()
        self.system_dbus = dbus.SystemBus()

    def session_object_methods(self):
        """
         可以调用应用所具有的方法
        :return: 方法的对象
        """
        proxy_object = self.session_dbus.get_object(self.dbus_name, self.object_path)
        object_methods = dbus.Interface(proxy_object, self.interface)
        return object_methods

    def session_object_properties(self):
        """
         可以获取应用所具有的属性
        :return: 属性的对象
        """
        proxy_object = self.session_dbus.get_object(self.dbus_name, self.object_path)
        object_properties = dbus.Interface(proxy_object, dbus.PROPERTIES_IFACE)
        return object_properties

    def set_session_properties_value(self, property_name, set_value):
        """
         设置属性的值
        :param property_name: 属性名称
        :return: 属性的值
        """
        self.session_object_properties().Set(self.interface, property_name, set_value)

    def get_session_properties_value(self, property_name):
        """
         获取应用属性的值
        :param property_name: 属性名称
        :return: 属性的值
        """
        value = self.session_object_properties().Get(self.interface, property_name)
        return value

    def get_system_properties_value(self, property_name):
        """
         获取系统dbus属性的值
        :param property_name: 属性名称
        :return: 属性的值
        """
        proxy_object = self.system_dbus.get_object(self.dbus_name, self.object_path)
        object_propertie = dbus.Interface(proxy_object, dbus.PROPERTIES_IFACE)
        return object_propertie.Get(self.interface, property_name)

    def system_object_methods(self):
        """
         可以调用应用所具有的方法
        :return: 方法的对象
        """
        proxy_object = self.system_dbus.get_object(self.dbus_name, self.object_path)
        object_methods = dbus.Interface(proxy_object, self.interface)
        return object_methods
