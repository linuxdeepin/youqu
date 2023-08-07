# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
"""Utility functions for 'dumping' trees of Node objects.

Author: Zack Cerza <zcerza@redhat.com>, Matěj Cepl <mcepl@redhat.com>"""
from io import StringIO

spacer = u' '


def dump_str(node):
    with StringIO as tmp_file:
        plain(node, output=tmp_file)
        dump_str = tmp_file.getvalue()
        return dump_str


def plain(node, output=None):
    """
    Plain-text dump. The hierarchy is represented through indentation.
    """
    close_output = False

    def crawl(node, depth):
        do_dump(node, depth)
        actions_keys = list(node.actions.keys())
        actions_keys.sort()
        for action in actions_keys:
            do_dump(node.actions[action], depth + 1)
        for child in node.children:
            crawl(child, depth + 1)

    def dumpFile(item, depth):
        _file.write(str(spacer * depth) + str(item) + str('\n'))

    def dumpStdOut(item, depth):
        try:
            print(spacer * depth + str(item))  # py3
        except UnicodeDecodeError:
            print(spacer * depth + str(item).decode('utf8'))  # py2 fallback

    _file = None

    if output:
        do_dump = dumpFile
        try:
            if hasattr(output, 'write'):
                _file = output
            elif isinstance(output, basestring):  # py2
                _file = open(output, 'w')
                close_output = True
        except NameError:
            if isinstance(output, str):  # there's no basestring in py3 (no str and unicode)
                _file = open(output, 'w')
                close_output = True
    else:
        do_dump = dumpStdOut

    crawl(node, 0)

    if close_output:
        _file.close()
