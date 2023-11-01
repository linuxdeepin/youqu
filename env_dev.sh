#!/bin/bash

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
source ./_env_base.sh

env(){
    sudo apt update

    deb_array=(
        python3-pip
        sshpass
        scrot
        python3-tk
        python3-pyatspi
        openjdk-8-jdk
        python3-opencv
    )

    # 裁剪基础环境
    cd ${ROOT_DIR}/src/utils
    BASICENV=$(python3 sub_env_cut.py)
    if [ "${BASICENV}" = "BASICENV" ]; then
        ENV_CUT_FLAG="cut"
        deb_array=(
            python3-pip
            sshpass
            openjdk-8-jdk
        )
    fi

    echo -e "${flag_feel}安装 deb 包\n"
    for deb in ${deb_array[*]}
    do
        sudo apt install -y ${deb} > /tmp/env.log 2>&1
        check_status ${deb}
    done

    # wayland
    if [ "${DISPLAY_SERVER}" = "wayland" ]; then
        wayland_env
    fi
}
# 默认源直接安装
env
# 如果安装过程中存在失败的情况，替换一下源再试一下
if [ "${env_retry}" = "true" ]; then
    # 适配专业版或社区版仓库源
    source /etc/os-release
    if [ "${NAME}" = "Deepin" ]; then
        community_sources_list
    else
        sources_list
    fi
    sudo mv /etc/apt/sources.list /etc/apt/sources.list.bak
    sudo cp sources.list /etc/apt/sources.list && rm -rf sources.list
    # 替换源之后再执行
    env
    sudo mv /etc/apt/sources.list.bak /etc/apt/sources.list
fi

pip_array=(
    pyscreeze==0.1.28
    PyAutoGUI==0.9.53
    pytest==6.2.5
    pytest-rerunfailures==10.2
    pytest-timeout==2.1.0
    allure-pytest==2.9.45
    pdocr-rpc
    allure-custom
    funnylog
    image-center
    letmego
)
# 裁剪基础环境
if [ "${ENV_CUT_FLAG}" = "cut" ]; then
    pip_array=(
        pytest==6.2.5
        pytest-rerunfailures==10.2
        pytest-timeout==2.1.0
        allure-pytest==2.9.45
        allure-custom
        funnylog
    )
fi
echo -e "${flag_feel}安装 pip 包\n"
sudo pip3 install -U pip > /tmp/env.log 2>&1
sudo pip3 config set global.timeout 10000 > /tmp/env.log 2>&1
sudo pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple > /tmp/env.log 2>&1
sudo pip3 config set global.extra-index-url https://it.uniontech.com/nexus/repository/pypi-public/simple

for p in ${pip_array[*]}
do
    sudo pip3 install ${p} > /tmp/env.log 2>&1
    check_status ${p}
    pip3 list | grep -v grep | grep ${p}
done
# 前面安装可能比较耗时，sudo免密可能出现过期，再输一把密码
echo "${PASSWORD}" | sudo -S su > /dev/null 2>&1
# 应用库新增Python依赖环境
cd ${ROOT_DIR}/src/utils/
requirements=$(python3 sub_depends.py)
if [ "${requirements}" != "" ]; then
    echo -e "\n应用库依赖:\n${requirements}\n"
    for requirement in ${requirements[*]}
    do
        echo -e "${flag_feel}安装应用库依赖: ${requirement}"
        sudo pip3 install -r ${requirement}
    done
fi

sudo pip3 install -U auto_uos --extra-index-url ${pypi_mirror} \
-i http://10.20.52.221:8081 --trusted-host=10.20.52.221 > /tmp/env.log 2>&1
check_status auto_uos
pip_show=$(pip3 show auto_uos | grep Location)
public_location=$(echo "${pip_show}" | cut -d ":" -f2 | python3 -c "s=input();print(s.strip())")
sudo rm -rf ${ROOT_DIR}/public
sudo cp -r ${public_location}/auto_uos ${ROOT_DIR}/public

system_env
cd ${ROOT_DIR};python3 manage.py run -h
