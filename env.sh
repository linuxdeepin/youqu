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
        python3-opencv
    )
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

echo -e "${flag_feel}安装 pip 包\n"
init_pip

sudo pip3 install pipenv > /tmp/env.log 2>&1
if [ $? = 0 ]; then
    echo -e "pipenv\t安装成功 √"
else
    echo -e "pipenv\t安装失败 ×"
    cat /tmp/env.log
    exit 520
fi
cd ${ROOT_DIR}/
pipenv --python 3.7 > /tmp/env.log 2>&1
if [ $? != 0 ]; then
    echo -e "AT环境创建失败"
    exit 521
fi
python_virtualenv_path=$(pipenv --venv)
whitelist_path=`echo "${python_virtualenv_path}" | sed "s/\/home\/$USER\//\//"`
result=`sudo cat ${whitelist} | grep ${whitelist_path}`
if [ -z "$result" ]; then
    sudo sed -i '$a\'"${whitelist_path}"'' ${whitelist}
    sudo sed -i '$a\'"${python_virtualenv_path}"'' ${whitelist}
    sudo systemctl restart deepin-elf-verify.service || true
fi

py_debs=(
    python3-gi
    python3-pyatspi
    python3-dbus
    python3-cairo
    python3-pil
    python3-ptyprocess
    python3-pexpect
    python3-numpy
    python3-opencv
)
for pd in ${py_debs[*]}
do
    rm -rf ${pd}*
    apt download ${pd} > /tmp/env.log 2>&1
    if [ $? != 0 ]; then
        cat /tmp/env.log
        exit 520
    fi
    dpkg -x ${pd}*.deb ${pd}
    cp -r ./${pd}/usr/lib/python3/dist-packages/* ${python_virtualenv_path}/lib/python3.7/site-packages/
    rm -rf ${pd}*
done

apt download python3-gi-cairo > /tmp/env.log 2>&1
dpkg -x python3-gi-cairo*.deb python3-gi-cairo
cp -r ./python3-gi-cairo//usr/lib/python3/dist-packages/gi/* ${python_virtualenv_path}/lib/python3.7/site-packages/gi/
rm -rf python3-gi-cairo*

pip_array=(
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
    letmego
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
    pipenv run pip list | grep -v grep | grep ${p}
done
echo "${PASSWORD}" | sudo -S su > /dev/null 2>&1
cd ${ROOT_DIR}/src/utils/
requirements=$(python3 sub_depends.py)
if [ "${requirements}" != "" ]; then
    echo -e "\n应用库依赖:\n${requirements}\n"
    for requirement in ${requirements[*]}
    do
        echo -e "${flag_feel}安装应用库依赖: ${requirement}"
        pipenv run pip install -r ${requirement} -i ${pypi_mirror}
    done
fi

pipenv run pip install -U auto_uos --extra-index-url ${pypi_mirror} -i http://10.20.52.221:8081 --trusted-host=10.20.52.221 \
> /tmp/env.log 2>&1
check_status auto_uos
pip_show=$(pipenv run pip show auto_uos | grep Location)
public_location=$(echo "${pip_show}" | cut -d ":" -f2 | python3 -c "s=input();print(s.strip())")
sudo rm -rf ${ROOT_DIR}/public
sudo cp -r ${public_location}/auto_uos ${ROOT_DIR}/public
sudo chmod -R 755 ${ROOT_DIR}/public

rm -rf Pipfile
echo "${python_virtualenv_path}"
pipenv run pip list
system_env

echo 'pipenv run python "$@"' | sudo tee /usr/bin/youqu > /dev/null 2>&1
echo "pipenv shell" | sudo tee /usr/bin/youqu-shell > /dev/null 2>&1
sudo chmod +x /usr/bin/youqu
sudo chmod +x /usr/bin/youqu-shell
cd ${ROOT_DIR};youqu manage.py run -h
