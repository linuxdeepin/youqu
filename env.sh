#!/bin/bash
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
export PIPENV_VERBOSITY=-1
ROOT_DIR=$(dirname $(realpath "${BASH_SOURCE[0]}"))
tag=$(echo "$(cat ${ROOT_DIR}/CURRENT | grep "tag = ")" | cut -d "=" -f2 | python3 -c "s=input();print(s.strip())")
config_pwd=$(cat ${ROOT_DIR}/setting/globalconfig.ini | grep -v "CLIENT_PASSWORD" | grep "PASSWORD = ")
PASSWORD=$(echo "${config_pwd}" | cut -d "=" -f2 | python3 -c "s=input();print(s.strip())")
DEV=false
while getopts ":p:D" opt
do
    case $opt in
        p)
            PASSWORD=$OPTARG
            ;;
        D)
            DEV=true
            ;;
        ?)
            echo -e " 参数说明:\
            \n\t-p password 指定密码, 如: bash env.sh -p xxx
            \n\t-D 开发环境部署, 如: bash env.sh -D
            "
            exit 1
            ;;
    esac
done

debian_platform=false
yq=apt
if command -v apt &> /dev/null; then
    debian_platform=true
    yq=apt
else
    yq=yum
fi

DISPLAY_SERVER=$(cat ${HOME}/.xsession-errors | grep XDG_SESSION_TYPE | head -n 1 | cut -d "=" -f2)
if [ "${DISPLAY_SERVER}" = "" ]; then
    ps -ef | grep -v grep | grep kwin_x11
    [ $? = 0 ] && DISPLAY_SERVER=x11 || DISPLAY_SERVER=wayland
fi
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
whitelist="/usr/share/deepin-elf-verify/whitelist"
pypi_mirror="https://pypi.tuna.tsinghua.edu.cn/simple"

echo "${PASSWORD}" | sudo -S su > /dev/null 2>&1

if [ ! -f "$HOME/.Xauthority" ]; then
        touch $HOME/.Xauthority
fi

if [ "${DEV}" = "true" ]; then
    source ./src/utils/env_dev.sh
else
    source ./src/utils/env_vir.sh
fi