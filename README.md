<p align="center">
  <a href="https://linuxdeepin.github.io/youqu">
    <img src="./docs/assets/logo.png" width="520" alt="YouQu">
  </a>
</p>
<p align="center">
    <em>YouQu（有趣），一个使用简单且功能强大的自动化测试基础框架。</em>
</p>




[![GitHub issues](https://img.shields.io/github/issues/linuxdeepin/youqu?color=%23F79431)](https://github.com/linuxdeepin/youqu/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/linuxdeepin/youqu?color=%23F79431)](https://github.com/linuxdeepin/youqu/pulls)
[![GitHub Discussions](https://img.shields.io/github/discussions/linuxdeepin/youqu?color=%23F79431)](https://github.com/linuxdeepin/youqu/discussions)

[![PyPI](https://img.shields.io/pypi/v/youqu?style=flat&logo=github&link=https%3A%2F%2Fpypi.org%2Fproject%2Fyouqu%2F&color=%23F79431)](https://pypi.org/project/youqu/)
![PyPI - License](https://img.shields.io/pypi/l/youqu?color=%23F79431)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/youqu?color=%23F79431)
![Static Badge](https://img.shields.io/badge/UOS%2FDeepin/Ubuntu/Debian-Platform?style=flat&label=OS&color=%23F79431)

[![Downloads](https://static.pepy.tech/badge/youqu/week)](https://pepy.tech/project/youqu)
[![Downloads](https://static.pepy.tech/badge/youqu/month)](https://pepy.tech/project/youqu)
[![Downloads](https://static.pepy.tech/badge/youqu)](https://pepy.tech/project/youqu)
[![Hits](https://hits.sh/github.com/linuxdeepin/youqu.svg?style=flat&label=Github_Hits&color=blue)](https://github.com/linuxdeepin/youqu)

---

<a href="https://github.com/linuxdeepin/youqu" target="_blank">GitHub</a> | <a href="https://gitee.com/deepin-community/youqu" target="_blank">Gitee</a>

<a href="https://linuxdeepin.github.io/youqu" target="_blank">在线文档</a>

---

YouQu（有趣）是深度公司开源的一个用于 Linux 操作系统的自动化测试框架，支持多元化元素定位和断言、用例标签化管理和执行、强大的日志和报告输出等特色功能，同时完美兼容 X11、Wayland 显示协议，环境部署简单，操作易上手。

## YouQu（有趣）能做什么

- [x] Linux 桌面应用 UI 自动化测试
- [x] Linux 桌面应用 DBus/Gsettings 接口自动化测试
- [x] 命令行自动化测试
- [x] HTTP 接口自动化测试
- [x] Web UI 自动化测试
- [ ] Linux 桌面应用性能自动化测试

<details>
	<summary style="color: #FF9933">点击查看爱上 “有趣（YouQu）” 的 N 个理由</summary>
	<ul>
        <li>无处不在的代码补全，让编写自动化测试用例成为一种享受；</li>
        <li>核心库提供了统一的接口，编写方法时只需要导入一个包就可以使用到核心库提供的所有功能；</li>
        <li>除了常用的属性定位、图像识别以外，我们还提供基于 UI 的元素定位方案，其使用简单且高效，效果一定能惊讶到你；</li>
        <li>对属性定位的方法进行了二次封装，将编写属性定位的方法变得简单而优雅；</li>
        <li>对图像识别定位技术进行功能升级，除了支持单个坐标返回，还支持同一界面下多个相同元素返回多个坐标的功能；</li>
        <li>提供用例标签化管理、批量跳过和批量条件跳过的功能，你想不到一个 csv 文件原来能干这么多事情；</li>
        <li>提供了功能强大的执行器入口，让你可以方便的在本地执行任何用例集的用例，其丰富的自定义配置项，满足你对执行器所有的幻想；</li>
        <li>提供远程执行的功能，可以控制多台机器并行跑，或者分布式跑，这种付费功能现在免费给你用；</li>
        <li>提供自动输出日志的功能，你再也不用为每个方法单独写输出日志的代码，一切我们给你搞定了，日志输出不仅内容丰富，颜值也绝对在线，我们还自己设计了一款终端输出主题叫《五彩斑斓的黑》；</li>
        <li>提供一键部署自动化测试环境的功能，让你再也不用为环境部署而烦恼；</li>
        <li>提供自动生成多种报告的功能，你想输出什么报告形式都行，而且我们在报告中还加入了失败录屏和失败截图的功能；</li>
        <li>对断言进行了二次封装，提供更友好化的错误提示，让定位问题精准高效；</li>
        <li>不仅支持单条用例超时控制，而且还支持动态控制用例批量执行的总时间，确保 CI 环境下能顺畅运行；</li>
        <li>支持本地文件测试套执行、PMS 测试套执行、标签化执行方案，满足你各种场景下的执行需求；</li>
        <li>支持基于深度学习的 OCR 功能，可定位可断言，中文识别的天花板；</li>
        <li>完美兼容 Wayland  和 X11，真正做到一套代码，随处执行；</li>
        <li>支持多种方式的数据回填功能，其中异步回填的方案，完美解决了数据回填的耗时问题；</li>
        <li>支持重启交互场景用例的执行，使用方法优雅简洁；</li>
    </ul>
</details>

## 安装

从 PyPI 安装:


```shell
$ sudo pip3 install youqu
```

## 创建项目

您可以在任意目录下，使用 `youqu-startproject` 命令创建一个项目：

```shell
$ youqu-startproject my_project
```

如果 `youqu-startproject` 后面不加参数，默认的项目名称为：`youqu` ；

![](./docs/assets/install.gif)

## 安装依赖

安装部署 YouQu 执行所需环境： 

```shell
$ cd my_project
$ bash env.sh
```

## 创建 APP 工程

使用 `startapp` 命令自动创建 APP 工程：

```shell
$ youqu manage.py startapp autotest_deepin_some
```

自动创建的 APP 工程遵循完整的 PO 设计模式，让你可以专注于用例和方法的编写维护。

在 `apps` 目录下会自动创建一个 APP 工程：`autotest_deepin_some`，同时新建好工程模板目录和模板文件：

```shell
my_project
├── apps
│   ├── autotest_deepin_some  # <----- APP 工程
...     ├── ...
```

在你的远程 Git 仓库中，只需要保存 APP 工程这部分代码即可。

`autotest_deepin_some` 是你的  APP 工程名称，在此基础上，你可以快速的开始你的 AT 项目，更重要的是确保创建工程的规范性。

`apps` 目录下可以存在任意多个 APP 工程。

运行
-------

### 1. 执行管理器

在项目根目录下有一个 `manage.py` ，它是一个执行器入口，提供了本地执行、远程执行等的功能。

### 2. 本地执行


```shell
$ youqu manage.py run
```

#### 2.1. 命令行参数

在一些 CI 环境下使用命令行参数会更加方便：


```shell
$ youqu manage.py run -a apps/autotest_deepin_some -k "xxx" -t "yyy"
```

更多用法可以使用 `-h` 或 `--help` 查看。

#### 2.2. 配置文件

通过配置文件配置参数

在配置文件 [setting/globalconfig.ini](https://github.com/linuxdeepin/youqu/blob/master/setting/globalconfig.ini)  里面支持配置对执行的一些参数进行配置。

### 3. 远程执行

远程执行就是用本地作为服务端控制远程机器执行，远程机器执行的用例相同。

使用 `remote` 命令：


```shell
$ youqu manage.py remote
```

## 贡献

[贡献文档](https://github.com/linuxdeepin/youqu/blob/master/CONTRIBUTING.md) 


## 开源许可证

YouQu 在 [GPL-2.0](https://github.com/linuxdeepin/youqu/blob/master/LICENSE) 下发布。
