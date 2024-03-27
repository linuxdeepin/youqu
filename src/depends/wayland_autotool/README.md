# wayland_autotool
## 安装依赖
```shell
sudo apt-get install -y g++ build-essential cmake qt5-default qt5-qmake libkf5wayland-dev libqt5gui5 libqt5core5a
```
## 编译
```shell
mkdir -p build && cd build && cmake .. && make -j4 && sudo make install
```
