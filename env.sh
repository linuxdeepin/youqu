#!/bin/bash

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
source ./_env_base.sh
echo "
 ██╗   ██╗  ██████╗      ███████╗ ███╗   ██╗ ██╗   ██╗
 ╚██╗ ██╔╝ ██╔═══██╗     ██╔════╝ ████╗  ██║ ██║   ██║
  ╚████╔╝  ██║   ██║     █████╗   ██╔██╗ ██║ ██║   ██║
   ╚██╔╝   ██║▄▄ ██║     ██╔══╝   ██║╚██╗██║ ╚██╗ ██╔╝
    ██║    ╚██████╔╝     ███████╗ ██║ ╚████║  ╚████╔╝
    ╚═╝     ╚══▀▀═╝      ╚══════╝ ╚═╝  ╚═══╝   ╚═══╝
    ${tag}
"

env(){
    sudo apt update

    deb_array=(
        python3-pip
        python3-tk
        sshpass
        scrot
        openjdk-8-jdk
        gir1.2-atspi-2.0
        libatk-adaptor
        at-spi2-core
        libcairo2-dev
        libdbus-glib-1-dev
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

    if [ "${DISPLAY_SERVER}" = "wayland" ]; then
        wayland_env
    fi
}
env
if [ "${env_retry}" = "true" ]; then
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
echo -e "${flag_feel}安装 pip 包\n"

sudo pip3 config set global.timeout 10000 > /tmp/env.log 2>&1
sudo pip3 config set global.index-url ${pypi_mirror} > /tmp/env.log 2>&1
sudo pip3 config set global.extra-index-url https://it.uniontech.com/nexus/repository/pypi-public/simple
sudo pip3 install pipenv > /tmp/env.log 2>&1
if [ $? = 0 ]; then
    echo -e "pipenv\t安装成功 √"
else
    echo -e "pipenv\t安装失败 ×"
    env_retry=true
    cat /tmp/env.log
    exit 520
fi
cd ${ROOT_DIR}/
pipenv --python 3.7
python_virtualenv_path=$(pipenv --venv)
#echo ${python_virtualenv_path}
whitelist_path=`echo "${python_virtualenv_path}" | sed "s/\/home\/$USER\//\//"`
result=`sudo cat ${whitelist} | grep ${whitelist_path}`
if [ -z "$result" ]; then
    sudo sed -i '$a\'"${whitelist_path}"'' ${whitelist}
    sudo sed -i '$a\'"${python_virtualenv_path}"'' ${whitelist}
    sudo systemctl restart deepin-elf-verify.service || true
fi

apt download python3-gi python3-pyatspi
dpkg -x python3-gi* gi
dpkg -x python3-pyatspi* pyatspi
cp -r ./gi/usr/lib/python3/dist-packages/* ${python_virtualenv_path}/lib/python3.7/site-packages/
sudo cp -r ./gi/usr/share/doc/* /usr/share/doc/
cp -r ./pyatspi/usr/lib/python3/dist-packages/* ${python_virtualenv_path}/lib/python3.7/site-packages/
sudo cp -r ./pyatspi/usr/share/doc/* /usr/share/doc/
rm -rf gi pyatspi python3*.deb

pip_array=(
    pycairo==1.16.2
    pygobject==3.30.4
    dbus-python==1.3.2
    xlib==0.21
    pillow==9.5.0
    pyscreeze==0.1.28
    PyAutoGUI==0.9.53
    pytest==6.2.5
    pytest-rerunfailures==10.2
    pytest-timeout==2.1.0
    allure-pytest==2.9.45
    funnylog
    pdocr-rpc
    image-center
    allure-custom
)

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

for p in ${pip_array[*]}
do
    pipenv run pip install ${p} -i ${pypi_mirror} > /tmp/env.log 2>&1
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
        pipenv run pip install -r ${requirement}
    done
fi
rm -rf Pipfile
system_env
echo "pipenv run python \$*" | sudo tee /usr/bin/youqu > /dev/null 2>&1
cd ${ROOT_DIR};youqu manage.py run -h
