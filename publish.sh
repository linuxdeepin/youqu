#!/bin/bash

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
cd ..
rm -rf publish_tmp
mkdir -p publish_tmp/youqu
cp -r deepin-autotest-framework/. publish_tmp/youqu/
rm -rf publish_tmp/youqu/.idea
rm -rf publish_tmp/youqu/.reuse
rm -rf publish_tmp/youqu/.gitignore
rm -rf publish_tmp/youqu/pyproject.toml
rm -rf publish_tmp/youqu/publish.sh
cp deepin-autotest-framework/pyproject.toml publish_tmp/
cd publish_tmp/
python3 -m build
twine upload dist/*