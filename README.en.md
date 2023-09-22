<p align="center">
&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
  <a href="https://linuxdeepin.github.io/deepin-autotest-framework/">
    <img src="https://pic.imgdb.cn/item/64f05326661c6c8e54fe9bf4.png" width="520" alt="YouQu">
  </a>
</p>

# YouQu

> YouQu, a simple and powerful autotest framework.

![PyPI](https://img.shields.io/pypi/v/youqu?style=flat&logo=github&link=https%3A%2F%2Fpypi.org%2Fproject%2Fyouqu%2F&color=%2344CC11)
![PyPI - License](https://img.shields.io/pypi/l/youqu?color=blue&color=%2344CC11)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/youqu?color=%2344CC11)
![Static Badge](https://img.shields.io/badge/UOS%2FDeepin/Ubuntu/Debian-Platform?style=flat&label=OS)
![Static Badge](https://img.shields.io/badge/Linux-Platform?style=flat&label=Platform)

[![Downloads](https://static.pepy.tech/badge/youqu/week)](https://pepy.tech/project/youqu)
[![Downloads](https://static.pepy.tech/badge/youqu/month)](https://pepy.tech/project/youqu)
[![Downloads](https://static.pepy.tech/badge/youqu)](https://pepy.tech/project/youqu)

English | [简体中文](README.md) 

YouQu is an automated testing basic framework designed and developed by Deepin Technology. It adopts the design concept of hierarchical structure, supports multiple element positioning and assertion, use case label management and execution, powerful log and report output and other special functions. At the same time, it is perfectly compatible with X11 and Wayland display protocols, the environment deployment is simple, and the operation is easy to use.

## Installation

- Installing from PyPI:

  ```shel
  sudo pip3 install youqu
  ```

  create a project:

  ```shell
  youqu-startproject my_project
  ```

  Installation dependencies:

  ```sh
  cd my_project
  bash env.sh
  ```

- Install from source code:

  ```sh
  git clone https://github.com/linuxdeepin/deepin-autotest-framework.git my_project
  cd my_project
  bash env.sh
  ```

## Usage

```sh
youqu manage.py run
```

## Documentations

- [Documents](https://linuxdeepin.github.io/deepin-autotest-framework/)

## Getting help

- [Official Forum](https://bbs.deepin.org/) for generic discussion and help.
- [Developer Center](https://github.com/linuxdeepin/developer-center) for BUG report and suggestions.
- [Wiki](https://wiki.deepin.org/)

## Getting involved

We encourage you to report issues and contribute changes

- [Contribution guide for developers](https://github.com/linuxdeepin/developer-center/wiki/Contribution-Guidelines-for-Developers-en) (English)
- [Translate for your language on Transifex](#) *please update to the actual Transifex link of this project*

## License

YouQu is licensed under [GPL-2.0-only](LICENSE)