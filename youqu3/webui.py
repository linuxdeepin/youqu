#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
from contextlib import contextmanager
from typing import Union

from youqu3 import setting
from youqu3.exceptions import YouQuPluginDependencyError

try:
    from playwright.sync_api import sync_playwright
    from playwright.sync_api import Page
    from playwright.sync_api import LocatorAssertions
    from playwright.sync_api import expect as _expect
    from playwright.sync_api import Locator
    from playwright.sync_api import APIResponse
    from playwright.sync_api import PageAssertions
    from playwright.sync_api import APIResponseAssertions
except ImportError:
    raise YouQuPluginDependencyError("playwright")


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
        locator: Union[Page, Locator, APIResponse],
    ) -> Union[PageAssertions, LocatorAssertions, APIResponseAssertions]:
        return _expect(locator)


@contextmanager
def debug_page():
    driver = sync_playwright().start()
    browser = driver.chromium.launch_persistent_context(
        user_data_dir=setting.USER_DATE_DIR,
        executable_path=setting.EXECUTABLE_PATH,
        ignore_https_errors=True,
        no_viewport=True,
        slow_mo=500,
        headless=setting.HEADLESS,
        bypass_csp=True,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--start-maximized",
        ],
    )
    _page = browser.pages[0]
    yield _page
    browser.close()
    driver.stop()
