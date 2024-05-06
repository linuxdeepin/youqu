## 创建一个 APP 工程

使用 startapp 创建一个 APP 工程：

```shell
youqu manage.py startapp autotest_my_app
```

![](/实践/startapp.gif)

自动创建 APP 工程，并生成大量模板代码：

```shell
autotest_my_project
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

## 修改

- 将方法层大目录 `widget` 修改为 `page` ， `widget` 目录下的文件名称、类名、函数名称，包含 `widget` 单词的地方都修改成 `page`。

- 添加 Web UI 项目标识文件：WEBUI

  ```shell
  touch WEBUI
  # WEB文件中不用写任何东西
  ```

最后移除掉一些不相关的文件：

```shell
autotest_my_project
├── apps
│   ├── autotest_my_app  # 创建的APP工程
│   │   ├── case
│   │   │   ├── assert_res  
│   │   │   │   └── readme
│   │   │   ├── base_case.py 
│   │   │   ├── __init__.py
│   │   │   ├── test_mycase_001.py  
│   │   │   └── test_mycase_002.py 
│   │   ├── WEBUI # Web UI 项目标识文件         <------------------ 非常重要
│   │   ├── config.ini 
│   │   ├── config.py  
│   │   ├── conftest.py 
│   │   ├── control 
│   │   ├── __init__.py
│   │   ├── my_app_assert.py 
│   │   ├── mycase.csv 
│   │   └── page  # 方法层
│   │       ├── base_page.py  # 方法基类
│   │       ├── case_res   # 用例执行所需要的资源
│   │       │   └── readme
│   │       ├── __init__.py
│   │       └── my_app_page.py  # 方法唯一出口类
```

## 再次执行 env.sh

```shell
cd my_project
bash env.sh
```

这样 Web UI 相关环境就准备好了。

## 编辑器打开

推荐使用 Pycharm 打开，并指定虚拟解释器：

![](/实践/桌面UI自动化/pc_open.gif)