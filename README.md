<p align="center">
  <a href="https://github.com/linuxdeepin/youqu">
    <img src="./docs/assets/logo.png" width="100" alt="YouQu3">
  </a>
</p>
<h1 align="center">YouQu3</h1>
<p align="center">
    <em>Next-Gen Linux Autotest Framework.</em>
</p>


![Python](https://img.shields.io/badge/Python-007CFF?style=for-the-badge&logo=Python&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-007CFF?style=for-the-badge&logo=linux&logoColor=white)

![PyPI](https://img.shields.io/pypi/v/youqu3?style=flat&logo=github&link=https%3A%2F%2Fpypi.org%2Fproject%2Fyouqu3%2F&color=%23F79431)
![Downloads](https://static.pepy.tech/badge/youqu3)
![Hits](https://hits.sh/github.com/linuxdeepin/youqu.svg?style=flat&label=visitors&color=blue)

--------------

文档：https://youqu.uniontech.com/v3/

--------------

**YouQu3** 是下一代 Linux 自动化测试框架，在继承 YouQu2 诸多亮点功能的同时解决其遇到的问题，同时对各功能进行插件化、模块化改造，全面优化框架接口调用机制。

## [特性]()

- 以 Python 包的形式提供框架能力，方便安装、更新。
- 自带虚拟环境管理器，支持离线部署，用例整体打包交付之后，可以在无网络环境下直接运行。
- 极致轻量化、可定制化依赖，可以根据测试项目类型安装对应的依赖。
- 功能可插拔，以插件的形式提供功能，不安装插件的情况下框架也能正常运行。
- 可视化配置，在浏览器中输入一些配置后即可驱动测试用例执行，搭配远程执行功能，可实现群控测试机执行。
- 支持非开发者下运行，简化系统环境部署。

## [安装]()

基础环境：

```shell
pip3 install youqu3
```

![](docs/assets/install.gif)

## 创建用例工程

创建一个目录

```bash
mkdir my_autotest
```

使用脚手架功能创建用例工程

```shell
cd my_autotest/
youqu3 init
```

![](docs/assets/init.gif)

## 开源许可证

YouQu3 在 [GPL-2.0](https://github.com/linuxdeepin/youqu/blob/main/LICENSE) 下发布
