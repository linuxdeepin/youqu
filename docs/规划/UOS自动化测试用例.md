---
Author : mikigo
---

# UOS 自动化测试用例

## 1. 简介

UOS 自动化测试用例，以下简称测试用例，是基于 YouQu3 和 UMTK 编写的 UOS 系统级测试用例，旨在提供 UOS 系统所有预装应用的测试用例。

## 2. 工程设计

### 2.1. 工程结构

```shell
uos-case
├── case 
│   ├── base_case.py
│   ├── dde_dock
│   │   ├── dock.csv
│   │   ├── __init__.py
│   │   └── test_dock_001.py
│   ├── dde_file_manager
│   │   ├── dfm.csv
│   │   ├── __init__.py
│   │   └── test_dfm_001.py
│   └── __init__.py
├── method
│   ├── assert_method.py
│   ├── base_method.py
│   ├── dde_dock_method.py
│   ├── dde_file_manager_method.py
│   ├── __init__.py
│   └── ui.ini
├── config.py
├── .env
├── LICENSE
├── pytest.ini
├── README.md
└── requirements.txt
```

### 2.2. 方案说明

- 系统中各应用在 case 目录下划分自己的用例模块，模块名称为应用包名，下划线连接单词。

- 用例中所需要的方法从 UMTK 里面导入使用，如果涉及到复杂步骤的封装，可以在方法层（method）做复杂步骤的封装。

  ```python
  from umtk.dde_file_manager import DdeFileManagerMethod
  from youqu3.gui import pylinuxauto
  ```

