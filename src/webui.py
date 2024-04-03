#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
from typing import Union

try:
    from playwright.sync_api import Page
    from playwright.sync_api import LocatorAssertions
    from playwright.sync_api import expect as _expect
    from playwright.sync_api import Locator
    from playwright.sync_api import APIResponse
    from playwright.sync_api import PageAssertions
    from playwright.sync_api import APIResponseAssertions
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


class WebAssert:

    @staticmethod
    def assert_locator(
            locator: Union[Page, Locator, APIResponse]
    ) -> Union[PageAssertions, LocatorAssertions, APIResponseAssertions]:
        return _expect(locator)
