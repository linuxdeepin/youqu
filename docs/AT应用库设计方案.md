# AT 应用库设计方案
```shell
# =================================================
# Author  : mikigo
# =================================================
```

## 一、目标

AT 应用库改造是基于自动化测试基础框架进行用例方法和业务逻辑的重新设计，以实现应用库高效的编写、维护用例及其方法。

## 二、方案设计

文件管理器从业务复杂度和用例量来讲，在系统所有应用中，是很有代表性的，难度也是最大的，因此我们选取文件管理器作为应用库改造的实验应用，给后续其他应用改造提供切实可行的思路和方案。

### 1、分层设计图

整体仍然遵循 PO 设计理念，根据业务需要，将文管业务层进行 3 层划分：

???+ note "应用库架构图（文件管理器）"
	![](https://pic.imgdb.cn/item/64f054c3661c6c8e54ff47db.png)

### 2、目录结构

```shell
autotest_dde_file_manager  # 应用仓库
├── case  # 用例
│   ├── assert_res  # 断言的图片资源目录
│   ├── test_xxx_001.py
│   ...
├── widget  # 方法
│   ├── __init__.py
│   ├── case_res  # 测试数据（用例需要用到的资源）
│   ├── pic_res  # 图像识别元素定位要用的图片
│   ├── base_widget.py  # 方法基类
│   ├── title_widget.py  # title 模块方法类
│   ├── right_view_widget.py  # right view 模块方法类
│   ├── left_view_widget.py  # left view 模块方法类
│   ├── pop_widget.py  # pop 模块方法类
│   ├── dfm_widget.py  # 方法的统一出口
│   └── ui.ini  # UI 定位的坐标配置文件
├── tag  # 用例标签目录
│   ├── xxx.csv  # 用例标签文件
│   ...
├── config.ini # 局部配置
├── config.py  # 局部配置
├── conftest.py  # Pytest 本地插件
└── dfm_assert.py  # 断言方法模块
```

## 三、详细方案

### 1、基类（base_widget.py）

- 继承核心层（src.Src）；
    ```python
    from src import Src
    
    class BaseWidget(Src):
    """方法基类"""
    
        APP_NAME = "dde-file-manager"
        DESC = "/usr/bin/dde-file-manager"
    
        def __init__(self, number=-1):
            Src.__init__(self, APP_NAME=self.APP_NAME, DESC=self.DESC, number=number)
    ```
- 抽取操作层的一些基础方法；
    - 元素定位操作的一些公共方法；
    - 路径组装方法；
- 一些**业务层**相关的变量、常量、shell命令、坐标；

### 2、操作层

- 模块划分

    按照文件管理器的界面区域划分为：==TitleWidget 、RightViewWidget、LeftViewWidget 、PopWidget== ；

    文管界面分为四个区域：==标题栏、右边视图区域、左边视图区域、弹窗[^1]==；

	[^1]: 设置界面弹窗、保险箱弹窗、删除确认弹窗、及各种网络弹窗.

	???+ note "主界面区域划分"
    	![](https://pic.imgdb.cn/item/64f054c3661c6c8e54ff4806.png)
	???+ note "弹窗区域"
    	![](https://pic.imgdb.cn/item/64f054c8661c6c8e54ff4d1b.png)


- 各个模块只继承基类

    ```python title="标题栏" hl_lines="1 3"
    from apps.autotest_dde_file_manager.widget import BaseWidget
  
    class TitleWidget(BaseWidget):
      """标题栏方法类"""
  
      def click_xxx_in_title_by_ui(self):
          # self.dog.find_element_by_attr("xxxx").click()
          self.click(*self.ui.btn_center("xxx"))
    ```
  
- 不同的定位方案调用不同的定位工具对象。

      ```python
      self.dog
      self.ui
      ```

- 方法编写

    - 动作开头，注意是动词

    ```python
    click
    double_click
    right_click
    get
    make
    ```

    - 元素对象名称

    	界面元素直接与元素名称相同，没有名称的就取一个好听易懂的名字。

    - 加上类的关键词

    	避免方法重名，同时可以标记区域。

    - 标定操作方法

        ```python
        by_ui
        by_attr
        by_mk
        by_img
        ```

### 3、应用层

- 继承操作层的所有类。

- 仅仅用于用例中导入方便，不做其他事情。

    ```python
    class DfmWidget(TitleWidget, RightViewWidget, LeftViewWidget, PopWidget):
		pass
    ```

- `DfmAssert`  直接在用例里面继承，方便使用断言语句。

    ```python hl_lines="2 4 7"
    from apps.dde_file_manager.widget.dfm_widget import DfmWidget
    from public.assert import Assert
  
    class DfmAssert(Assert):
  
        def assert_file_exists_in_desktop(self, file_name):
            self.assert_file_exists(f"~/Desktop{file_name}")
            ...
            DfmWidget().get_file_in_desktop()
    ```

  - 用例里面直接继承，方便在用例里面使用 self 进行断言，更符合断言的使用习惯，用例逻辑上更清楚。

    ```python hl_lines="1 3" title="case/base_case.py"
    from apps.autotest_dde_file_manager.dfm_assert import DfmAssert
    
    class BaseCase(DfmAssert):
		pass
    ```
    
    ```python hl_lines="1 3 5" title="case/test_xxx_001.py"
    from apps.autotest_dde_file_manager.case import BaseCase
    
    class TestFileManager(BaseCase):
        def test_xxx_001(self):
            self.assert_file_exists_in_desktop("xxx")
    ```

### 4、逻辑举例

用例代码调用逻辑举例：

```python title="widget/base_widget.py"
class BaseWidget(Src):
    """方法基类"""
    APP_NAME = "dde-file-manager"
    DESC = "/usr/bin/dde-file-manager"

    def __init__(self, number=-1):
        Src.__init__(self, APP_NAME=self.APP_NAME, DESC=self.DESC, number=number)
```

```python title="widget/title_widget.py"
from apps.autotest_dde_file_manager.widget import BaseWidget

class TitleWidget(BaseWidget):

    def __init__(self, nubmer=-1):
        BaseWidget.__init__(self, nubmer=nubmer)

    def click_xxx_title_by_ui(self):
        print(self.dog.app_name)
        self.ui.print_number()
```

```python title="widget/right_view_widget.py"
from apps.autotest_dde_file_manager.widget import BaseWidget

class RightViewWidget(BaseWidget):

    def __init__(self, nubmer=-1):
        BaseWidget.__init__(self, nubmer=nubmer)

    def click_xxx_right_by_ui(self):
        print(self.dog.app_name)
        self.ui.print_number()
```

```python title="widget/dfm_widget.py"
from apps.autotest_dde_file_manager.widget import TitleWidget
from apps.autotest_dde_file_manager.widget import RightViewWidget

class DfmWidget(TitleWidget, RightViewWidget):
    pass
```

```python title="case/test_xxx_002.py"
from apps.dde_file_manager.widget import DfmWidget
from apps.autotest_dde_file_manager.case import BaseCase

class TestDdeFileManager(BaseCase):
	
	def test_xxx_002(self):
        dfm = DfmWidget()
        dfm.click_xxx_title_by_ui()
        dfm.click_xxx_right_by_ui()
        dfm.dog.print_desc()
        dfm.ui.print_number()
```

## 四、工程改造实施步骤

### 1、基础框架代码拉取

1.1. 将自动化基础框架的功能拉到本地（参考《快速开始》章节）

1.2. 将应用库代码拉到基础框架下 `apps` 目录下，应用库的仓库命名应该是长这样的 `autotest_deepin_xxx`。

### 2、调整工程目录

按照 `方案设计-目录结构` 进行目录调整，尽量使用编辑器进行相应的调整，编辑器推荐使用 `Pycharm` ，以下操作均在 `Pycharm` 里面可实现。

2.1. 需要移动 `py` 文件或目录，直接在编辑器里面，使用鼠标选中并按住，之后拖动到目标位置即可，`Pycharm` 会尽可能的自动解决移动导致的路径问题。注意，我说的是“尽可能”，有些骚操作编辑器是无法自动处理的。如果没有被编辑器自动处理的路径问题，后续只能手动解决。

2.2. 需要重命名文件或目录，在编辑器里面选中文件，然后使用快捷键 `Shift + F6` （如果快捷键没反应，文件右键菜单  `Refactor —— Rename`），然后在输入框中输入要重命名的名称，同时，确认勾选 `Search for references` 和 `Search in comments and strings` 这两个选项，最后按回车或者鼠标点 `Refactor` 。

注意，此时编辑器可能会提示你，你这个重命名的操作关联了多个模块，它被多个地方都使用到了，相关的模块是否也一起改名了，这不废话吗，用这个功能就是想把关联到的都修改，不然我为什么不用文管的重命名功能呢，别想了，直接点左下角的 `Refactor` 按钮，就是干。

类名、函数名的重命名都尽量采用这种方案，因为编辑器会自动给我们找到关联的地方，然后同步修改掉。你可千万别直接删了修改名称，不然你可能会花上一天的时间来解决重命名的问题。

### 3、实现核心库接口

3.1. `BaseWidget`

在 `BaseWidget` 里面把该写的都写好，你可以参考上面的设计理念来写。

如果你嫌麻烦，你可以参考文件管理器的实际工程代码 `autotest_dde_file_manager` :   [https://gerrit.uniontech.com/admin/repos/autotest_dde_file_manager](https://gerrit.uniontech.com/admin/repos/autotest_dde_file_manager ) 

3.2. 操作层

如果你是新写项目，你会发现一切都是那么的简单、直接，按照我们提供给你的接口写用例的操作方法就好了。

如果你是想对原来的工程进行改造，你需要按照核心库方法的调用，将你之前写的每个方案进行对应的修改，包括类和方法的命名、方法内所要用到不同定位方法的写法修改。

这时候你可能你的代码中可能会有一些报错，不用担心，你可以从业务逻辑出发，想清楚这个方法是干什么的、操作的对象是什么、参数是什么，注意这些修改是会影响到用例代码里面的，没关系，用例里面本来也应该被关联修改。

3.3. 把配置模块写好，这部分基本可以复制文管的代码。

### 4、路径处理

4.1. 导入路径

方法和用例中都会涉及到导入路径的修改，在修改路径时，建议你使用 `Ctrl + Shift + R` 全局替换，会将整个项目下的相同地方都修改到，当然，你也可以在小弹窗中修改全局替换为局部目录下替换。处理那种没有关联关系，但是又是相同名称的重命名，我也推荐使用这种方式进行重命名。

注意，全局替换的方式任然无法保证真的全局被替换了（可能是编辑器的 Bug 吧），所以你仍然需要手动看下各处是否修改到位。

4.2. 资源路径

一些用例资源需要根据 `config.py` 里面的路径配置进行资源路径的拼接，如果你原来本来就有一个函数专门用于组装路径的，那你只需要修改这一个地方就好了，如果你之前并没有这样的设计，那可能需要修改大量涉及到资源路径的地方。

### 5、调试和编写用例

以上几个步骤做完，基本就可以进行用例代码的调试了，这部分工作主要解决你之前几个步骤遗漏的问题，如果所有用例都调试通过了，那么工程改造就全部完成了。
