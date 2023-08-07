
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
echo "1" | sudo -S su
sudo apt update
sudo apt install -y g++ build-essential cmake qt5-default qt5-qmake libkf5wayland-dev libqt5gui5 libqt5core5a
mkdir -p build && cd build && cmake .. && make -j4 && sudo make install