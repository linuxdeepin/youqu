---
Author : mikigo
---

# UOS 自动化测试方法套件（UMTK）

## 1. 简介

UOS 自动化测试方法套件，全称：UOS 系统自动化测试操作方法套件（`UOS  AutoTest Method ToolKit` —— **`UMTK`**），以下简称测试方法套件，是基于 YouQu3 封装的 UOS 操作系统预装应用的元素操作方法套件。

测试方法套件是一个独立项目，旨在提供系统预装应用所有的元素的操作方法，这些元素操作方法可以用于自动化用例调用，组装成自动化测试用例。

## 2. 工程设计

### 2.1. 工程结构

```shell
uos-method-toolkit
├── LICENSE
├── README.md
├── tests
└── umtk
    ├── dde_file_manager
    │   ├── dde_file_manager_method.py
    │   └── __init__.py
    ├── deepin_music
    │   ├── deepin_music_method.py
    │   └── __init__.py
    ├── deepin_movie
    │   ├── deepin_music_method.py
    ... ...
    └── __init__.py
```

### 2.2. 方案说明

- 系统中各应用划分自己的模块，模块名称为应用包名，下划线连接单词。

- 每个应用存在一个唯一的出口文件，供外部用例调用。

  ```python
  from umtk.dde_file_manager import DdeFileManagerMethod
  ```

  `DdeFileManagerMethod` 可以调用  `dde-file-manager` 所有的元素操作方法。

- 所有方法以类的形式编写，遵循 PO 设计模式。

- 测试方法套件中所有的方法均为原子操作，不做复杂步骤的封装。

## 3. 套件发布

- 套件分大版本发布，比如 V20、V25 是不同的测试方法套件版本，在不同的代码仓库中。

- 在同一个大版本中，套件持续保持更新，并在系统关键节点发布对应的版本；

  比如 V20 阶段，1070 发布一个套件版本，1071 发布一个套件版本，以此类推，过程中如果根据需要出小版本。

- 套件通过 PyPI 发布，用户可直接通过 pip 命令安装使用：

  安装：

  ```shell
  pip install umtk
  ```

  使用：

  ```python
  from umtk.dde_file_manager import DdeFileManagerMethod
  ```

## 4. 套件维护

- 套件由专人主责维护（maintainer），其他人可以提需求、issue、PR，以保持套件的各方面一致性。

- 鼓励内外部开发者贡献 PR。

## 5. 对套件的测试

套件里面保存元素的操作方法，在操作方法多了之后，维护方法的稳定性有效性将成为一个问题。

因此，我们需要建立对套件的自动化测试，专门针对元素操作方法函数进行测试，类似于单元测试。

适配厂商可以直接使用这些单元测试进行适配测试。

## 6. UMTK 和 YouQu2 的公共方法库（public）有何区别

> 孔子《论语·卫灵公》: “道，不同，不相为谋。” 

亦各从其志也。

**使用的框架不同**

- YouQu2 的公共方法库（public）是在 YouQu2 的框架下进行开发的，它不能脱离 YouQu2 框架而独立使用。
- UMTK 是基于 YouQu3 开发，YouQu3 采用全新的架构设计，和 YouQu2 有很大差异，因此 UMTK 和 public 二者属于两个时代，不兼容。

**内容、范围、业务不同**

- UMTK 涵盖了 UOS 系统所有预装应用的原子操作方法，不存在复杂步骤的堆叠封装，不受需求变更影响，不涉及用例逻辑，可以对外开源发布。
- public 仅包含自动化用例用到的少部分公共方法，范围覆盖很少，且存在较多涉及用例逻辑的复杂步骤方法，容易受到需求变更，不适合对外开源发布。

**代码一致性**

- UMTK 所有代码由专人维护，且有完善的单元测试机制，确保操作方法的一致性、稳定性、有效性。
- public 大量人员都可以对其进行直接修改，各种代码风格不统一，稳定性、有效性没有保障。