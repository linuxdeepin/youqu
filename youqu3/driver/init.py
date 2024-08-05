#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import os
import pathlib
import re
import shutil
from time import strftime

from youqu3 import setting


class Init:

    @staticmethod
    def copy_template_to_apps():
        os.system(f"cp -r {setting.TPL_PATH}/* .")
        os.system(f"cp {setting.TPL_PATH}/.gitignore-tpl  .")

    @classmethod
    def init(cls):
        cls.copy_template_to_apps()
        dirname = pathlib.Path(".").absolute().name
        for root, dirs, files in os.walk("."):
            for file in files:
                app_name = dirname.lower()

                if file.endswith("-tpl"):

                    if "${app_name}" in file:
                        new_file = re.sub(
                            r"\${app_name}", app_name, file
                        )
                        shutil.move(f"{root}/{file}", f"{root}/{new_file}")
                        file = new_file

                    if ".py-tpl" in file or ".csv-tpl" in file:
                        with open(f"{root}/{file}", "r") as f:
                            codes = f.readlines()
                        new_codes = []
                        for code in codes:
                            if "${APP_NAME}" in code:
                                code = re.sub(r"\${APP_NAME}", app_name.upper(), code)
                            if "${app_name}" in code:
                                code = re.sub(r"\${app_name}", app_name, code)
                            if "${AppName}" in code:
                                code = re.sub(r"\${AppName}", app_name.title().replace("_", "").replace("-", ""), code)
                            if "${USER}" in code:
                                code = re.sub(r"\${USER}", setting.USERNAME, code)
                            if "${DATE}" in code:
                                code = re.sub(r"\${DATE}", strftime("%Y/%m/%d"), code)
                            if "${TIME}" in code:
                                code = re.sub(r"\${TIME}", strftime("%H:%M:%S"), code)
                            if "${FIXEDCSVTITLE}" in code:
                                code = re.sub(
                                    r"\${FIXEDCSVTITLE}",
                                    ",".join([i.value for i in setting.FixedCsvTitle]),
                                    code,
                                )
                            new_codes.append(code)
                        with open(f"{root}/{file}", "w") as f:
                            f.writelines([i for i in new_codes])

                    shutil.move(f"{root}/{file}", f"{root}/{file[:-4]}")


class Tree:
    class Node:
        def __init__(self, name):
            self.name = name
            self.children = []

        def add_child(self, child):
            if child not in self.children:
                self.children.append(child)

        def __repr__(self, ):
            return str(self.name)

    def __init__(self, root_name, edges):
        self.edges = edges
        self.root = self._build_tree(root_name)
        self.tree_plot = ''

    def _build_tree(self, root_name):
        root = self.Node(root_name)
        for e in self.edges:
            if e[0] == root_name:
                root.add_child(self._build_tree(e[1]))
        return root

    def _tree(self, node, prefix=[]):
        space = '     '
        branch = '│   '
        tee = '├─ '
        last = '└─ '

        if len(prefix) == 0:
            self.tree_plot = ''

        self.tree_plot += ''.join(prefix) + str(node) + '\n'

        if len(prefix) > 0:
            prefix[-1] = branch if prefix[-1] == tee else space

        for i, e in enumerate(node.children):
            if i < len(node.children) - 1:
                self._tree(e, prefix + [tee])
            else:
                self._tree(e, prefix + [last])

        return self.tree_plot

    def __repr__(self):
        return self._tree(self.root)


def print_tree():
    from youqu3 import version
    print(f"The project has been init by YouQu3-{version}")
    edges = []
    for root, dirs, files in os.walk("."):
        dirs.sort()
        files.sort()
        if root.startswith(("./.idea", "./.vscode")):
            continue
        _dirname = os.path.split(os.path.abspath(root))[-1]
        for dir in dirs:
            if dir in (".idea", ".vscode"):
                continue
            edges.append((_dirname, dir))
        for file in files:
            if file in ("readme", "__init__.py"):
                continue
            edges.append((_dirname, file))

    dirname = pathlib.Path(".").absolute().name
    print(Tree(dirname, edges))
