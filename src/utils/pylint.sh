#! /bin/bash

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
CUR_DIR=$(pwd)
ROOT_DIR=$(dirname "$(dirname "$(pwd)")")
echo -e "\n====================== youqu pylint 代码扫描 ========================"
config_pwd=$(cat ${ROOT_DIR}/setting/globalconfig.ini | grep "PASSWORD = ")
PASSWORD=$(echo "${config_pwd}" | cut -d "=" -f2 | python3 -c "s=input();print(s.strip())")
export PYTHONPATH=`pwd`
# 检查安装
pylint --version > /dev/null 2>&1
[ $? -ne 0 ] && pip3 install pylint -i https://pypi.tuna.tsinghua.edu.cn/simple
pip3 list | grep pylint-json2html  > /dev/null 2>&1
[ $? -ne 0 ] && pip3 install pylint-json2html -i https://pypi.tuna.tsinghua.edu.cn/simple
# 配置代码检查的目录
if [ -d $1 ] || [ -f $1 ]; then
    check_dir=$1
else
    echo "$1 不是一个文件或目录，请输入需要扫描的目录，默认目录从项目根目录开始
    比如：apps/autotest_deepin_music"
    read -p "(Enter扫描整个项目)：" check_dir
fi

# 代码检查的目录(绝对路径)
abs_check_path="${ROOT_DIR}/${check_dir}"

if [ -d "${abs_check_path}" ] || [ -f "${abs_check_path}" ]; then
    echo -e "正在扫描 \033[32m${abs_check_path}\033[0m ..."
    if [ ! -d "${ROOT_DIR}/report" ];then mkdir "${ROOT_DIR}/report";fi
    report_path="${ROOT_DIR}/report/pylints"
    if [ ! -d ${report_path} ]; then
        mkdir -p ${report_path}
    fi
    report_file=${report_path}/pylint_$(date "+%Y-%m-%d_%H:%M:%S").html
    pylint --rcfile=${ROOT_DIR}/setting/pylintrc.cfg ${abs_check_path} | \
    pylint-json2html -o ${report_file}
    echo -e "请查看扫描报告：\033[32m ${report_file}\033[0m\n"
else
    echo -e "\033[41;30m <${abs_check_path}> 目录不存在 \033[0m\n"
fi
