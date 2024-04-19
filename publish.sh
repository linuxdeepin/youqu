#!/bin/bash
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only

tmp_publish_dir_name=_youqu_publish_tmp_dir
cd ..
rm -rf ${tmp_publish_dir_name}
mkdir -p ${tmp_publish_dir_name}/youqu/apps/
ls youqu | grep -v apps | grep -v public | grep -v report | xargs -i cp -r youqu/{} ${tmp_publish_dir_name}/youqu/
cp youqu/apps/__init__.py ${tmp_publish_dir_name}/youqu/apps/
rm -rf ${tmp_publish_dir_name}/youqu/.idea
rm -rf ${tmp_publish_dir_name}/youqu/.vscode
rm -rf ${tmp_publish_dir_name}/youqu/.pytest_cache
rm -rf ${tmp_publish_dir_name}/youqu/.reuse
rm -rf ${tmp_publish_dir_name}/youqu/pyproject.toml
rm -rf ${tmp_publish_dir_name}/youqu/publish.sh
rm -rf ${tmp_publish_dir_name}/youqu/deploy.sh
rm -rf ${tmp_publish_dir_name}/youqu/site
rm -rf ${tmp_publish_dir_name}/youqu/docs
rm -rf ${tmp_publish_dir_name}/youqu/README.en.md
rm -rf ${tmp_publish_dir_name}/youqu/CONTRIBUTING.md
rm -rf ${tmp_publish_dir_name}/youqu/LICENSE
rm -rf ${tmp_publish_dir_name}/youqu/RELEASE.md
rm -rf ${tmp_publish_dir_name}/youqu/mkdocs.yml
rm -rf ${tmp_publish_dir_name}/youqu/requirements*.txt
rm -rf ${tmp_publish_dir_name}/youqu/apps/autotest*
rm -rf ${tmp_publish_dir_name}/youqu/Pipfile
rm -rf ${tmp_publish_dir_name}/youqu/Pipfile.lock
rm -rf ${tmp_publish_dir_name}/youqu/ci_result.json
cp youqu/pyproject.toml ${tmp_publish_dir_name}/
cp youqu/src/startproject.py ${tmp_publish_dir_name}/youqu/
cd ${tmp_publish_dir_name}/
python3 -m build
#twine upload dist/*