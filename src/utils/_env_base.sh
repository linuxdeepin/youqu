#!/bin/bash
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only

ctrl_c_handler(){
    echo "正在退出……"
    exit 1
}

trap ctrl_c_handler INT

check_status(){
    if [ $? = 0 ]; then
        echo -e "$1\t安装成功 √"
    else
        echo -e "$1\t安装失败 ×"
        cat /tmp/env.log
    fi
}

wayland_env(){
    deb_array=(g++ build-essential cmake qt5-default qt5-qmake libqt5gui5 libqt5core5a wl-clipboard)
    for deb in ${deb_array[*]}
    do
        sudo apt install -y ${deb} > /tmp/env.log 2>&1
        check_status ${deb}
        apt policy ${deb} > /tmp/_yqdebversion.txt 2>&1
        cat /tmp/_yqdebversion.txt | grep "已安装"
    done

    # 根据 libkf5waylandclient5 的版本决定安装 libkf5wayland-dev 的版本;
    libkf5waylandclient5_version=$(apt policy libkf5waylandclient5 | grep "已安装" | python3 -c "s=input();print(s.split('：')[1])")
    sudo apt install -y libkf5wayland-dev=${libkf5waylandclient5_version} > /tmp/env.log 2>&1
    wayland_info="libkf5wayland-dev 可能存在依赖报错，解决方法：\n
    方案一. 添加镜像对应的 ppa 仓库源，重新执行；\n
    方案二. sudo aptitude install libkf5wayland-dev,先输 n,再输 y,再输 y \n
    ***方案二可能引入兼容性问题，慎用，在下非常非常非常不推荐。***"
    echo -e ${wayland_info} >> /tmp/env.log 2>&1
    check_status libkf5wayland-dev

    # 编译工具
    cd ${ROOT_DIR}/src/depends/wayland_autotool/
    mkdir -p build && cd build
    cmake .. > /dev/null 2>&1
    make -j4 > /dev/null 2>&1
    sudo make install > /dev/null 2>&1
    [ $? = 0 ] && tool_status="成功 √" || tool_status="失败 ×"
    echo -e "wayland_autotool 安装${tool_status}"
    # 添加wayland下有用的环境变量，其实框架执行的时候底层也会自动判断并添加，这里咱们先打个提前量；
    cat $HOME/.bashrc | grep 'export GDMSESSION=Wayland' > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "export QT_WAYLAND_SHELL_INTEGRATION=kwayland-shell" >> $HOME/.bashrc
        echo "export XDG_SESSION_DESKTOP=Wayland" >> $HOME/.bashrc
        echo "export XDG_SESSION_TYPE=wayland" >> $HOME/.bashrc
        echo "export WAYLAND_DISPLAY=wayland-0" >> $HOME/.bashrc
        echo "export GDMSESSION=Wayland" >> $HOME/.bashrc
        echo 'export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/1000/bus"' >> $HOME/.bashrc
    fi
    wayland_cmd_path="/usr/local/bin/wayland_autotool"
    result=`sudo cat ${whitelist} | grep ${wayland_cmd_path}`
    if [ -z "$result" ]; then
        sudo sed -i '$a\'"${wayland_cmd_path}"'' ${whitelist} || echo "白名单${whitelist}写入失败"
        sudo systemctl restart deepin-elf-verify.service || true
    fi

    nohup wayland_autotool > /dev/null 2>&1 &
}

system_env(){
    echo "${PASSWORD}" | sudo -S su  > /dev/null 2>&1
    sudo sed -i "s/#PubkeyAuthentication yes/PubkeyAuthentication yes/g" /etc/ssh/sshd_config > /dev/null 2>&1
    sudo sed -i "s/#   StrictHostKeyChecking ask/   StrictHostKeyChecking no/g" /etc/ssh/ssh_config  > /dev/null 2>&1
    cat $HOME/.bashrc | grep 'export DISPLAY=":0"' > /dev/null 2>&1
    if [ $? -ne 0 ]; then
         echo 'export PIPENV_VERBOSITY=-1' >> $HOME/.bashrc
         echo 'export DISPLAY=":0"' >> $HOME/.bashrc
         echo 'export QT_QPA_PLATFORM=' >> $HOME/.bashrc
         echo 'export QT_ACCESSIBILITY=1' >> $HOME/.bashrc
         echo 'export QT_LINUX_ACCESSIBILITY_ALWAYS_ON=1' >> $HOME/.bashrc
    fi
    source $HOME/.bashrc
    echo "cd ${ROOT_DIR}/src/depends/sniff/;python3 sniff" | sudo tee /usr/bin/sniff > /dev/null 2>&1
    sudo chmod +x /usr/bin/sniff

    gsettings set org.gnome.desktop.interface toolkit-accessibility true  > /dev/null 2>&1
    sudo systemctl enable ssh  > /dev/null 2>&1
    sudo systemctl start ssh  > /dev/null 2>&1
}

init_pip(){
    sudo pip3 config set global.index-url ${pypi_mirror} > /tmp/env.log 2>&1
    sudo pip3 install -U pip > /tmp/env.log 2>&1
    sudo pip3 cache purge > /tmp/env.log 2>&1
    sudo pip3 config set global.timeout 10000 > /tmp/env.log 2>&1
}

install_py_deb(){
    rm -rf ${1}*
    ${yq} download ${1} > /tmp/env.log 2>&1
    if [ $? != 0 ]; then
        cat /tmp/env.log
        exit 120
    fi
    dpkg -x ${1}*.deb ${1}
    cp -r ./${1}/usr/lib/python3/dist-packages/* ${2}/lib/python${PYTHON_VERSION}/site-packages/
    rm -rf ${1}*
}
