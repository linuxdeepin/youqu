#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
try:
    from playwright.sync_api import Page
except ImportError:
    print("Please install playwright")


class WebUI:

    def __init__(self, page: Page):
        self.page = page

    def goto(self, url):
        self.page.goto(url)

    def input_text(self, element, text):
        self.page.fill(element, text)

    def click_element(self, element):
        self.page.click(element)
