#!/bin/bash

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
source ${ROOT_DIR}/src/utils/_env_base.sh

export PIPENV_VENV_IN_PROJECT=true
export PIPENV_PYPI_MIRROR=https://pypi.tuna.tsinghua.edu.cn/simple
export PIPENV_QUIET=true
export PIPENV_DEFAULT_PYTHON_VERSION=3

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
    if [ "${debian_platform}" = "true" ]; then
        sudo apt update
    fi

    deb_array=(
        python3-pip
        python3-tk
        scrot
        openjdk-11-jdk-headless
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

    if [ "${DISPLAY_SERVER}" = "wayland" ]; then
        wayland_env
    fi
}
env

init_pip

sudo pip3 install pipenv > /tmp/env.log 2>&1
if [ $? = 0 ]; then
    echo -e "pipenv\t安装成功 √"
else
    echo -e "pipenv\t安装失败 ×"
    cat /tmp/env.log
    exit 120
fi
cd ${ROOT_DIR}/
pipenv --python ${PYTHON_VERSION} > /tmp/env.log 2>&1
if [ $? != 0 ]; then
    echo -e "AT环境创建失败"
    exit 121
fi
python_virtualenv_path=$(pipenv --venv)
whitelist_path=`echo "${python_virtualenv_path}" | sed "s;${HOME};;g"`
if [ -f "${whitelist}" ]; then
    result=`sudo cat ${whitelist} | grep ${whitelist_path}`
    if [ -z "$result" ]; then
        sudo sed -i '$a\'"${whitelist_path}"'' ${whitelist}
        sudo sed -i '$a\'"${python_virtualenv_path}"'' ${whitelist}
        sudo systemctl restart deepin-elf-verify.service || true
    fi
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
    install_py_deb ${pd} ${python_virtualenv_path}
done

${yq} download python3-gi-cairo > /tmp/env.log 2>&1
dpkg -x python3-gi-cairo*.deb python3-gi-cairo
cp -r ./python3-gi-cairo/usr/lib/python3/dist-packages/gi/* ${python_virtualenv_path}/lib/python${PYTHON_VERSION}/site-packages/gi/
rm -rf python3-gi-cairo*

cd ${ROOT_DIR}/src/utils/
sub_py_debs=$(python3 sub_deb.py)
for spd in ${sub_py_debs[*]}
do
    install_py_deb ${spd} ${python_virtualenv_path}
done

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

cd ${ROOT_DIR}/src/utils/
webui=$(python3 sub_webui.py)
if [ "${webui}" != "" ]; then
    pipenv run pip install playwright -i ${pypi_mirror}
    pipenv run playwright install chromium
fi

cd ${ROOT_DIR}/src/utils/
remote=$(python3 sub_remote.py)
if [ "${remote}" != "" ]; then
    pipenv run pip install zerorpc -i ${pypi_mirror}
fi

pipenv run pip install -U auto_uos --extra-index-url ${pypi_mirror} -i http://10.20.52.221:8081 --trusted-host=10.20.52.221 \
> /tmp/env.log 2>&1
check_status auto_uos
pip_show=$(pipenv run pip show auto_uos | grep Location)
public_location=$(echo "${pip_show}" | cut -d ":" -f2 | python3 -c "s=input();print(s.strip())")
sudo rm -rf ${ROOT_DIR}/public
sudo cp -r ${public_location}/auto_uos ${ROOT_DIR}/public
sudo chmod -R 777 ${ROOT_DIR}/public

cd ${ROOT_DIR}
rm -rf Pipfile
echo "${python_virtualenv_path}"
pipenv run pip list
system_env

echo 'pipenv run python "$@"' | sudo tee /usr/bin/youqu > /dev/null 2>&1
echo "pipenv shell" | sudo tee /usr/bin/youqu-shell > /dev/null 2>&1
echo "pipenv --rm" | sudo tee /usr/bin/youqu-rm > /dev/null 2>&1
sudo chmod +x /usr/bin/youqu
sudo chmod +x /usr/bin/youqu-shell
sudo chmod +x /usr/bin/youqu-rm

cd ${ROOT_DIR};youqu manage.py -h
