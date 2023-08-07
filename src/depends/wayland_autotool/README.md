# wayland_autotool
> 南研提供的wayland下键鼠操作的服务端，使用时需要提前在测试机上进行安装
## 安装依赖
```shell
sudo apt-get install -y g++ build-essential cmake qt5-default qt5-qmake libkf5wayland-dev libqt5gui5 libqt5core5a
```
## 编译
```shell
mkdir -p build && cd build && cmake .. && make -j4 && sudo make install
```
