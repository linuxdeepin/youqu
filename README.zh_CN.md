![](https://raw.githubusercontent.com/mikigo/pic/main/logo.png)

# 有趣

> 有趣，是一个使用简单且功能强大的自动化测试基础框架。

![PyPI](https://img.shields.io/pypi/v/youqu?style=flat&logo=github&link=https%3A%2F%2Fpypi.org%2Fproject%2Fyouqu%2F)
![PyPI - License](https://img.shields.io/pypi/l/youqu)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/youqu)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/youqu)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/youqu)
![Static Badge](https://img.shields.io/badge/UOS%2FDeepin-Platform?style=flat-square&label=OS)
![Static Badge](https://img.shields.io/badge/Linux-Platform?style=flat-square&label=Platform)

[![Downloads](https://static.pepy.tech/badge/youqu/week)](https://pepy.tech/project/youqu)
[![Downloads](https://static.pepy.tech/badge/youqu/month)](https://pepy.tech/project/youqu)
[![Downloads](https://static.pepy.tech/badge/youqu)](https://pepy.tech/project/youqu)
![GitHub repo size](https://img.shields.io/github/repo-size/linuxdeepin/deepin-autotest-framework)

[English](README.md) | 简体中文

有趣（YouQu）是深度科技设计和开发的一个自动化测试基础框架，采用结构分层的设计理念，支持多元化元素定位和断言、用例标签化管理和执行、强大的日志和报告输出等特色功能，同时完美兼容X11、Wayland显示协议，环境部署简单，操作易上手。

## 安装

- 从 PyPI 安装:

  ```shel
  sudo pip3 install youqu
  ```

  创建项目:

  ```shell
  youqu-startproject my_project
  ```

  安装依赖:

  ```sh
  cd my_project
  bash env.sh
  ```

- 从源码安装:

  ```sh
  git clone https://github.com/linuxdeepin/deepin-autotest-framework.git my_project
  cd my_project
  bash env.sh
  ```

### 使用

```sh
youqu manage.py run
```

## 文档

- [文档](https://linuxdeepin.github.io/deepin-autotest-framework/)

## 帮助

- [官方论坛](https://bbs.deepin.org/) 
- [开发者中心](https://github.com/linuxdeepin/developer-center) 
- [Wiki](https://wiki.deepin.org/)

## 贡献指南

我们鼓励您报告问题并做出更改

- [开发者代码贡献指南](https://github.com/linuxdeepin/developer-center/wiki/Contribution-Guidelines-for-Developers) 

## 开源许可证

有趣 在 [GPL-2.0-only](LICENSE) 下发布。