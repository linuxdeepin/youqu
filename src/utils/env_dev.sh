#!/bin/bash
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
source ${ROOT_DIR}/src/utils/_env_base.sh

env(){

    if [ "${debian_platform}" = "true" ]; then
        sudo apt update
    fi

    deb_array=(
        python3-pip
        scrot
        python3-tk
        python3-pyatspi
        openjdk-11-jdk-headless
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
            openjdk-11-jdk-headless
        )
    fi

    if [ "${debian_platform}" = "false" ]; then
        deb_array[${#deb_array[@]}]=java-11-openjdk-headless
        deb_array[${#deb_array[@]}]=python3-tkinter
        deb_array[${#deb_array[@]}]=xdotool
        deb_array[${#deb_array[@]}]=opencv
    fi

    for deb in ${deb_array[*]}
    do
        sudo ${yq} install -y ${deb} > /tmp/env.log 2>&1
        check_status ${deb}
    done

    cd ${ROOT_DIR}/src/utils/
    sub_py_debs=$(python3 sub_deb.py)
    for spd in ${sub_py_debs[*]}
    do
        sudo ${yq} install -y ${spd} > /tmp/env.log 2>&1
        check_status ${spd}
    done

    # wayland
    if [ "${DISPLAY_SERVER}" = "wayland" ]; then
        wayland_env
    fi
}
env

init_pip

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

if [ ${debian_platform} == false ]; then
        pip_array[${#pip_array[@]}]=numpy
        pip_array[${#pip_array[@]}]="pillow==8.4.0"
        pip_array[${#pip_array[@]}]=pexpect
    fi

for p in ${pip_array[*]}
do
    sudo pip3 install ${p} > /tmp/env.log 2>&1
    check_status ${p}
    pip3 list | grep -v grep | grep ${p}
done
echo "${PASSWORD}" | sudo -S su > /dev/null 2>&1
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

cd ${ROOT_DIR}/src/utils/
webui=$(python3 sub_webui.py)
if [ "${webui}" != "" ]; then
    sudo pip3 install playwright -i ${pypi_mirror}
    playwright install chromium
fi

cd ${ROOT_DIR}/src/utils/
remote=$(python3 sub_remote.py)
if [ "${remote}" != "" ]; then
    sudo pip3 install zerorpc -i ${pypi_mirror}
fi

sudo pip3 install -U auto_uos --extra-index-url ${pypi_mirror} -i http://10.20.52.221:8081 --trusted-host=10.20.52.221 \
> /tmp/env.log 2>&1
check_status auto_uos
pip_show=$(pip3 show auto_uos | grep Location)
public_location=$(echo "${pip_show}" | cut -d ":" -f2 | python3 -c "s=input();print(s.strip())")
sudo rm -rf ${ROOT_DIR}/public
sudo cp -r ${public_location}/auto_uos ${ROOT_DIR}/public
sudo chmod -R 777 ${ROOT_DIR}/public

system_env
