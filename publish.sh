#!/bin/bash
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only

tmp_publish_dir_name=_youqu_publish_tmp_dir
cd ..
rm -rf ${tmp_publish_dir_name}
mkdir -p ${tmp_publish_dir_name}/youqu/apps/
ls youqu | grep -v apps | grep -v public | grep -v report| grep -v node_modules | xargs -i cp -r youqu/{} ${tmp_publish_dir_name}/youqu/
cp youqu/apps/__init__.py ${tmp_publish_dir_name}/youqu/apps/

ignores=(
    .idea
    .vscode
    .pytest_cache
    .reuse
    pyproject.toml
    publish.sh
    deploy.sh
    site
    docs
    README.en.md
    CONTRIBUTING.md
    LICENSE
    RELEASE.md
    mkdocs.yml
    requirements*.txt
    apps/autotest*
    Pipfile
    Pipfile.lock
    ci_result.json
    package.json
    pnpm-lock.yaml
)
for i in ${ignores[*]}
do
    rm -rf rm -rf ${tmp_publish_dir_name}/youqu/${i}
done
cp youqu/pyproject.toml ${tmp_publish_dir_name}/
cp youqu/src/startproject.py ${tmp_publish_dir_name}/youqu/
cd ${tmp_publish_dir_name}/
python3 -m build
#twine upload dist/*
