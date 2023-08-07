#!/bin/bash

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
install_pycharm_community(){
    PYCHARM="pycharm-community-2020.3.5"
    cd /opt/
    sudo wget --timeout=300 https://cdimage.uniontech.com/daily-iso/source/tool/${PYCHARM}.tar.gz
    sudo tar -xzvf ${PYCHARM}.tar.gz
    sudo rm -rf ${PYCHARM}.tar.gz
    cd -
    sudo touch /usr/share/applications/pycharm.desktop
    echo "
    [Desktop Entry]
    Version=1.0
    Type=Application
    Name=PyCharm Community Edition
    Icon=/opt/${PYCHARM}/bin/pycharm.svg
    Exec=sh /opt/${PYCHARM}/bin/pycharm.sh
    Comment=Python IDE for Professional Developers
    Categories=Development;IDE;
    Terminal=false
    StartupWMClass=jetbrains-pycharm-ce
    X-Deepin-CreatedBy=com.deepin.dde.daemon.Launcher
    X-Deepin-AppID=jetbrains-pycharm-ce
    " | sudo tee /usr/share/applications/pycharm.desktop
}

if [ -f /usr/share/applications/pycharm.desktop ]; then
    echo "Pycharm Exists!"
else
    install_pycharm_community
fi
