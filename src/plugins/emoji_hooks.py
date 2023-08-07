#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
import pytest


# 自定义hook


@pytest.hookspec(firstresult=True)
# pylint: disable=unused-argument
def pytest_emoji_passed(config, head_line):
    """pytest_emoji_passed"""


@pytest.hookspec(firstresult=True)
# pylint: disable=unused-argument
def pytest_emoji_failed(config, head_line):
    """pytest_emoji_failed"""


@pytest.hookspec(firstresult=True)
# pylint: disable=unused-argument
def pytest_emoji_skipped(config, head_line):
    """pytest_emoji_skipped"""


@pytest.hookspec(firstresult=True)
# pylint: disable=unused-argument
def pytest_emoji_error(config, head_line):
    """pytest_emoji_error"""


# @pytest.hookspec(firstresult=True)
# def pytest_emoji_xfailed(config):
#     ...
#
#
# @pytest.hookspec(firstresult=True)
# def pytest_emoji_xpassed(config):
#     ...
