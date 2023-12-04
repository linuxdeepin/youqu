<p align="center">
  <a href="https://linuxdeepin.github.io/deepin-autotest-framework/">
    <img src="./docs/logo.png" width="520" alt="YouQu">
  </a>
</p>

<p align="center">
    <em>有趣，一个使用简单且功能强大的自动化测试基础框架。</em>
</p>

![PyPI](https://img.shields.io/pypi/v/youqu?style=flat&logo=github&link=https%3A%2F%2Fpypi.org%2Fproject%2Fyouqu%2F&color=%23F79431)
![PyPI - License](https://img.shields.io/pypi/l/youqu?color=%23F79431)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/youqu?color=%23F79431)
![Static Badge](https://img.shields.io/badge/UOS%2FDeepin/Ubuntu/Debian-Platform?style=flat&label=OS&color=%23F79431)
![Static Badge](https://img.shields.io/badge/Linux-Platform?style=flat&label=Platform&color=%23F79431)

[![Downloads](https://static.pepy.tech/badge/youqu/week)](https://pepy.tech/project/youqu)
[![Downloads](https://static.pepy.tech/badge/youqu/month)](https://pepy.tech/project/youqu)
[![Downloads](https://static.pepy.tech/badge/youqu)](https://pepy.tech/project/youqu)

---

**文档**: <a href="https://linuxdeepin.github.io/deepin-autotest-framework" target="_blank">https://linuxdeepin.github.io/deepin-autotest-framework</a>

**源码**: <a href="https://github.com/linuxdeepin/deepin-autotest-framework" target="_blank">https://github.com/linuxdeepin/deepin-autotest-framework</a>

---

有趣（YouQu）是深度科技开源的一个用于 `Deepin/UOS` 操作系统（Linux）的自动化测试框架，采用结构分层的设计理念，支持多元化元素定位和断言、用例标签化管理和执行、强大的日志和报告输出等特色功能，同时完美兼容X11、Wayland显示协议，环境部署简单，操作易上手。

### 爱上 “有趣” 的 18 个理由

1. 核心库提供了统一的接口，编写方法时只需要导入一个包就可以使用到核心库提供的所有功能；
2. 公共库封装了很多常用模块的相关方法，比如：任务栏的操作、桌面的操作、右键菜单的操作等等；
3. 除了常用的属性定位、图像识别以外，我们还提供基于 `UI` 的元素定位方案，其使用简单且高效，效果一定能惊讶到你；
4. 对属性定位的方法进行了二次封装，将编写属性定位的方法变得简单而优雅；
5. 对图像识别定位技术进行功能升级，除了支持单个坐标返回，还支持同一界面下多个相同元素返回多个坐标的功能；
6. 提供用例标签化管理、批量跳过和批量条件跳过的功能，你想不到一个 `csv` 文件原来能干这么多事情；
7. 提供了功能强大的执行器入口，让你可以方便的在本地执行任何用例集的用例，其丰富的自定义配置项，满足你对执行器所有的幻想；
8. 提供远程执行的功能，可以控制多台机器并行跑，或者分布式跑，这种付费功能现在免费给你用；
9. 提供自动输出日志的功能，你再也不用为每个方法单独写输出日志的代码，一切我们给你搞定了，日志输出不仅内容丰富，颜值也绝对在线，我们还自己设计了一款终端输出主题叫《五彩斑斓的黑》；
10. 提供一键部署自动化测试环境的功能，让你再也不用为环境部署而烦恼；
11. 提供自动生成多种报告的功能，你想输出什么报告形式都行，而且我们在报告中还加入了失败录屏和失败截图的功能；
12. 对断言进行了二次封装，提供更友好化的错误提示，让定位问题精准高效；
13. 不仅支持单条用例超时控制，而且还支持动态控制用例批量执行的总时间，确保 `CI` 环境下能顺畅运行；
14. 支持本地文件测试套执行、`PMS` 测试套执行、标签化执行方案，满足你各种场景下的执行需求；
15. 支持基于深度学习的 `OCR` 功能，可定位可断言，中文识别的天花板；
16. 完美兼容 `Wayland`  和 `X11`，真正做到一套代码，随处执行；
17. 支持多种方式的数据回填功能，其中异步回填的方案，完美解决了数据回填的耗时问题；
18. 支持重启交互场景用例的执行，使用方法优雅简洁；

------------------------

【[视频介绍](https://doc.uniontech.com/file/gXqmeOpjg4uGpRqo)】

统信公司内网还可以访问【[内网文档](http://youqu-dev.uniontech.com/)】，文档内容一样，访问速度更快哦~~

## 安装使用

从 PyPI 安装:

```shel
sudo pip3 install youqu
```

创建项目:

```shell
youqu-startproject my_project
```

如果 `youqu-startproject` 后面不加参数，默认的项目名称为：`youqu` ；

安装依赖:

```sh
cd my_project
bash env.sh
```

> 注意，如果你的测试机密码不是 1 ，那你需要在全局配置文件 `globalconfig.ini` 里面将 `PASSWORD` 配置项修改为当前测试机的密码。

-------------------------------

**【APP工程】**

如果您已经有一个可用的 `APP` 工程，将应用库放到基础框架下 `apps` 目录下，像这样：

```shell
my_project
├── apps
│   ├── autotest_deepin_music  # 应用库
...
```

`APP` 工程名称应该以 `autotest_` 开头，请不要随意修改 `APP` 工程名称；

如果您还没有 `APP` 工程，建议使用框架提供的脚手架功能创建一个全新的 `APP` 工程。

## 创建工程

创建一个 APP 工程：

```shell
youqu manage.py startapp autotest_deepin_some  
```

这样在 `apps` 目录下会创建一个子项目工程 `autotest_deepin_some`，同时新建好工程模板目录和模板文件：

```shell
apps
└── autotest_deepin_some
    ├── case
    │   ├── assert_res
    │   │   └── readme
    │   ├── base_case.py
    │   └── __init__.py
    ├── config.ini
    ├── config.py
    ├── conftest.py
    ├── control
    ├── deepin_some_assert.py
    ├── deepin_some.csv
    ├── __init__.py
    └── widget
        ├── base_widget.py
        ├── case_res
        │   └── readme
        ├── deepin_some_widget.py
        ├── __init__.py
        ├── other.ini
        ├── other_widget.py
        ├── pic_res
        │   └── readme
        └── ui.ini
```

`autotest_deepin_some` 是你的工程名称，比如：`autotest_deepin_music` ；

在此基础上，你可以快速的开始你的 AT 项目，更重要的是确保创建工程的规范性。

运行
-------

### 1. 工作空间

在项目根目录下有一个 `manage.py` ，它是一个执行器入口，提供了本地执行、远程执行等的功能。

### 2. 本地执行

```shell
youqu manage.py run
```

#### 2.1. 命令行参数

通过命令行参数配置参数，使用 `-h` 或 `--help` 可以查看所有支持的命令行参数：

```shell
youqu manage.py run -h
```

在一些 CI 环境下使用命令行参数会更加方便：

```shell
youqu manage.py run --app apps/autotest_deepin_music --keywords "xxx" --tags "xxx"
```

更多参数请查看【[命令行参数](https://linuxdeepin.github.io/deepin-autotest-framework/%E6%A1%86%E6%9E%B6%E5%8A%9F%E8%83%BD%E4%BB%8B%E7%BB%8D/%E6%89%A7%E8%A1%8C%E7%AE%A1%E7%90%86%E5%99%A8/#21)】

#### 2.2. 配置文件

通过配置文件配置参数

在配置文件 `setting/globalconfig.ini` 里面支持配置对执行的一些参数进行配置，配置完成之后，直接在命令行执行 `manage.py` 就好了。

详细配置项请查看【[配置项](https://linuxdeepin.github.io/deepin-autotest-framework/%E6%A1%86%E6%9E%B6%E5%8A%9F%E8%83%BD%E4%BB%8B%E7%BB%8D/%E6%89%A7%E8%A1%8C%E7%AE%A1%E7%90%86%E5%99%A8/#22)】

### 3. 远程执行

远程执行就是用本地作为服务端控制远程机器执行，远程机器执行的用例相同；

使用 `remote` 命令：

```shell
youqu manage.py remote
```

#### 3.1. 远程多机器分布式异步执行

![](https://pic.imgdb.cn/item/64f6d3c0661c6c8e549f8ca5.png)

多机器分布式异步执行就是由本地 YouQu 作为服务端，控制远程 N 台机器执行相同的用例，执行完之后所有测试机的测试结果会返回给服务端 report 目录下；

远程执行同样通过配置文件 `setting/globalconfig.ini` 进行用例相关配置；

需要重点说一下远程执行时的测试机信息配置，在配置文件 `setting/remote.ini`  里面配置测试机的用户名、IP、密码。

```ini
;=============================== CLIENT LIST =====================================
; 测试机配置列表
;[client{number}]     ;测试机别名，有多少台测试机就写多少个 client，别名必须包含 client 字符，且不能重复。
;user =               ;测试机 user
;ip =                 ;测试机 ip
;password = 1         ;测试机的密码, 可以不配置此项，默认取 CLIENT_PASSWORD 的值；
                      ;如果你所有测试机密码都相同，那么只需要配置 CLIENT_PASSWORD 就可以了
;=================================================================================

[client1]
user = uos
ip = 10.8.15.xx

[client2]
user = uos
ip = 10.8.15.xx

[client3]
user = uos
ip = 10.8.11.xx
```

有多少台机器就像这样参考上面的格式写就行了。

然后在命令行：

```shell
youqu manage.py remote
```

这样运行是从配置文件去读取相关配置。

如果你不想通过配置文件，你仍然通过命令行参数进行传参，

以下为 `python3 manage.py remote` 提供的一些参数选项：

```coffeescript
  -h, --help            show this help message and exit
  -c CLIENTS, --clients CLIENTS
                        远程机器的user@ip:password,多个机器用'/'连接,如果password不传入,默认取sett
                        ing/remote.ini中CLIENT_PASSWORD的值,比如: uos@10.8.13.xx:1
                        或 uos@10.8.13.xx
  -s, --send_code       发送代码到测试机（不含report目录）
  -e, --build_env       搭建测试环境,如果为yes，不管send_code是否为yes都会发送代码到测试机.
  -p CLIENT_PASSWORD, --client_password CLIENT_PASSWORD
                        测试机密码（全局）
  -y PARALLEL, --parallel PARALLEL
                        yes:表示所有测试机并行跑，执行相同的测试用例;no:表示测试机分布式执行，服务端会根据收集到的测试用例自
                        动分配给各个测试机执行。
```

**除了这些特有参数以外，它同样支持本地执行的所有参数；**

在命令行这样运行：

```shell
youqu manage.py remote -a apps/autotest_deepin_music -c uos@10.8.13.x3/uos@10.8.13.x4 -k "xxx" -t "xxx"
```

所有用例执行完之后会在 `report` 目录下回收各个测试机执行的测试报告。

注意，如果远程机器没有搭建自动化测试环境，记得加上参数 `-e` ：

```shell
youqu manage.py remote -a ... -e
```

执行前确保远程机器已经开启了 ssh 服务，否则会提示无法连接，如果没有开启，请手动开启：

```shell
sudo systemctl restart ssh
sudo systemctl enable ssh
```

配置文件其他相关配置项详细说明，请查看配置文件中的注释内容。

#### 3.2. 远程多机器分布式异步负载均衡执行

多机器分布式异步负载均衡执行也是用本地作为服务端控制远程机器执行，但远程机器执行的用例不同，而是所有远程机器执行的用例之和，为你想要执行的用例集；

似乎有点难以理解，我用大白话举例描述下：

服务端想要执行 10 条用例，现在远程机器有 5 台，然后服务端就先拿着第 1 条用例给远程 1 号机执行，拿第 2 条用例给远程 2 号机执行...，如此循环直到所有用例执行完，这就是负载均衡执行。

![](https://pic.imgdb.cn/item/64f6d694661c6c8e54a1025b.png)

使用方法和前面一样，只是需要增加一个参数 `--parallel`：

```shell
youqu manage.py remote -a ... --parallel no
```

## 帮助

- [官方论坛](https://bbs.deepin.org/) 
- [开发者中心](https://github.com/linuxdeepin/developer-center) 
- [Wiki](https://wiki.deepin.org/)

## 贡献指南

我们鼓励您报告问题并做出更改

- [开发者代码贡献指南](https://github.com/linuxdeepin/developer-center/wiki/Contribution-Guidelines-for-Developers) 

## 开源许可证

有趣 在 [GPL-2.0-only](https://github.com/linuxdeepin/deepin-autotest-framework/blob/master/LICENSE) 下发布。
