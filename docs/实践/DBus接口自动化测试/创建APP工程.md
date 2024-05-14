# 创建一个 APP 工程

使用 startapp 创建一个 APP 工程：

```shell
youqu manage.py startapp autotest_my_app
```

![](/实践/startapp.gif)

自动创建 APP 工程，并生成大量模板代码：

```shell
my_project
├── apps
│   ├── autotest_my_app  # 创建的APP工程
│   │   ├── case  # 用例目录
│   │   │   ├── assert_res  # 用例断言所需要的资源
│   │   │   │   └── readme
│   │   │   ├── base_case.py  # 用例基类
│   │   │   ├── __init__.py
│   │   │   ├── test_mycase_001.py  # 用例示例 1
│   │   │   └── test_mycase_002.py  # 用例示例 2
│   │   ├── config.ini  # 应用库配置文件
│   │   ├── config.py   # 读取配置文件config.ini里面的配置，并提供可调用的配置对象config
│   │   ├── conftest.py  # Pytest Fixture 插件库
│   │   ├── control  # 记录依赖YouQu的版本
│   │   ├── __init__.py
│   │   ├── my_app_assert.py  # 断言方法类
│   │   ├── mycase.csv  # 用例标签管理文件
│   │   └── widget  # 方法层
│   │       ├── base_widget.py  # 方法基类
│   │       ├── case_res   # 用例执行所需要的资源
│   │       │   └── readme
│   │       ├── __init__.py
│   │       ├── my_app_widget.py  # 方法唯一出口类
│   │       ├── other.ini  # 其他应用的基于相对位移元素定位方案的配置文件
│   │       ├── other_widget.py   # 其他方法类
│   │       ├── pic_res  # 图像识别方法所需要的资源
│   │       │   └── readme
│   │       └── ui.ini  # 相对位移元素定位方案的配置文件
```

## 编辑器打开

推荐使用 Pycharm 打开，并指定虚拟解释器：

![](/实践/桌面UI自动化/pc_open.gif)