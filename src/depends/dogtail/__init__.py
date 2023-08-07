# -*- coding: UTF-8 -*-
# This file was modified by UnionTech Software Technology Co., Ltd. in 2022/08/11
"""
# ==============================================
# huangmingqiang@uniontech.com
# Time: 2022/8/11
# 官方仓库 https://gitlab.com/dogtail/dogtail/
# 里面有0.9.11的版本，经过流水线测试，偶现一些奇怪的报错，
# 在pypi里面只发布了0.9.10，因此我们仍然使用0.9.10稳定版本，
# 在源代码基础上，我们新增了Wayland下的键操作支持，以兼容
# Wayland模式下的自动化用例执行。
# ==============================================
"""
from __future__ import absolute_import, division, print_function, unicode_literals
# pylint: disable=W0105,C0413,C0114
"""
GUI test tool and automation framework that uses Accessibility (a11y) technologies to communicate
with desktop applications.
"""

__author__ = """Zack Cerza <zcerza@redhat.com>,
Ed Rousseau <rousseau@redhat.com>,
David Malcolm <dmalcolm@redhat.com>,
Vita Humpa <vhumpa@redhat.com>"""
__version__ = "0.9.10"
__copyright__ = "Copyright © 2005-2017 Red Hat, Inc."
__license__ = "GPL"

__all__ = ("config", "distro", "dump", "errors", "i18n", "logging", "path", "predicate",
           "procedural", "rawinput", "sessions", "tc", "tree", "utils", "version", "wrapped")


__contributor__ = "Mikigo <huangmingqiang@uniontech.com>"

import os
import sys

DEPENDS_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, DEPENDS_PATH)
