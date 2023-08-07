#!/bin/bash

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
# VNC connect
sudo apt install x11vnc -y
sudo x11vnc -storepasswd 1 /etc/x11vnc.pass
vnc_connect(){
sudo bash -c 'cat << EOF > "/lib/systemd/system/x11vnc.service"

[Unit]
Description=Start x11vnc at startup
After=multi-user.target
[Service]
Type=simple
ExecStart=/usr/bin/x11vnc -auth guess -forever -loop -noxdamage -repeat -rfbauth /etc/x11vnc.pass -rfbport 5900 -shared
[Install]
WantedBy=multi-user.target
EOF'
}
vnc_connect
sudo chmod 755 /lib/systemd/system/x11vnc.service
sudo chown root:root /lib/systemd/system/x11vnc.service
sudo systemctl enable x11vnc.service
sudo systemctl daemon-reload
sudo systemctl start x11vnc.service