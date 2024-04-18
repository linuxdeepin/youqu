# AT 基础框架设计方案

```shell
# ====================================
# Author  : mikigo
# ====================================
```

## 一、目标

做一个简单、好用、功能强大的自动化测试框架。

- 作为自动化测试的一个基础框架，任何应用都能很方便的接入进来；
- 提供所有自动化测试所需要的底层功能，并对外提供唯一的接口，方便应用库使用；
- 整合公共库，减少应用库代码量和方法维护。

## 二、设计方案

### 1、统一概念

- **基础框架**

  本项目是一个自动化测试的基础框架（`AutoTest Basic Frame`），全称为“自动化测试基础框架（AT 基础框架）”。

  AT 基础框架是做为一个自动化测试的基础框架来设计的，它提供了自动化测试所要用的基础功能，任何应用接入进来都能快速方便的进行方法和用例编写，同时在用例标签化管理、批量跳过、标签化执行、分布式执行、多种报告输出、优美的执行日志、失败自动录屏和截图、自动环境清理等等，它都提供了完善的解决方案，更重要的是这一切使用起来都非常简单。

  基础框架中包含应用库（`apps`）、核心库（`src`）、公共方法库（`public`）。

- **应用库（`apps`）**

  各个应用自己的仓库，里面主要包含的是用例、方法及一些测试资源，比如文件管理器叫 `autotest-dde-file-manager` 。

- **核心库（`src`）**

  核心库自动化测试所要用的到所有底层核心功能，这是最重要的一个部分，灵魂。具体功能模块及说明会在下面第四个章节详细描述。

- **公共方法库（`public`）**

  多个应用都要用到的一些操作方法，按照应用划分存放，主要是为了减少代码量，消除应用间的耦合关系。

### 2、架构图

整体的框架设计在《自动化测试架构设计》文档里面已经有详细描述了，这里贴一下整体的架构图：

???+ note "架构图"
	![](https://pic.imgdb.cn/item/64f054c4661c6c8e54ff4948.png)

为了突显本文的重点，抽取其中重要功能模块，如下图：

???+ note "核心模块"
	![](https://pic.imgdb.cn/item/64f054c2661c6c8e54ff4770.png)

### 3、目录结构

```shell title="框架结构"
autotest-basic-frame  # 自动化测试基础框架
├── apps  # 应用库
│   ├── autotest-dde-file-manager  # 单独的应用仓库（应用库详细目录结构请看应用库设计方案）
│   │   ├── case  # 用例
│   │   ├── config.ini # 局部配置
│   │   ├── config.py  # 局部配置
│   │   ├── conftest.py  # Pytest 本地插件
│   │   ├── dfm_assert.py  # 断言方法模块
│   │   ├── assert_res  # 断言的图片资源
│   │   ├── tag  # 标签
│   │   └── widget  # 方法库
│   │       ├── __init__.py
│   │       ├── base_widget.py
│   │       ├── ui.ini  # UI 定位的坐标配置文件
│   │       ├── case_res  # 测试数据（用例需要用到的资源）
│   │       └── pic_res  # 图像识别元素定位要用的图片
│   │           ├── xxx.png
│   │           ...
│   ├── autotest_deepin_music  # 单独的应用仓库
│   │  ├── case
│   │  ├── ...
│   ...
├── public  # 公共方法库
│   ├── __init__.py
│   ├── dde_dock_public_widget  # dde_dock 的公共方法 package
│   │   ├── __init__.py
│   │   ├── dde_dock_public_widget.py
│   │   ├── ui.ini 
│   │   └── res 
│   ├── dde_desktop_public_widget  # dde_desktop 的公共方法 package
│   │   ├── __init__.py
│   │   ├── dde_desktop_public_widget.py
│   │   ├── ui.ini 
│   │   └── res 
│   ...
├── src  # 核心库
│   ├── __init__.py
│   ├── button_center.py
│   ├── cmdtrl.py
│   ├── dogtails.py
│   ├── find_image.py
│   ├── global_config.py
│   ├── ...
│   ...
├── setting  # 全局配置模块
│   ├── __init__.py
│   ├── globalconfig.py
│   └── globalconfig.ini
├── conftest.py  # Pytest 本地插件模块（Hook）
├── pytest.ini  # Pytest 默认配置文件
├── docs  # 文档目录
└── manage.py  # 执行器
```

## 三、详细方案

### 1、==应用库（apps）==

所有应用库均放置在基础框架下的 `apps` 目录下（见第二章节第3段目录结构内容）。应用库的架构设计可以参考《AT 应用库设计方案》文档。

### 2、==核心库（src）==

在 `src` 目录下为自动化测试的底层核心组件，通常来讲如果你需要使用到其中某一个功能模块，那么你需要显示的导入这个模块，然后才能使用该模块下的功能，如果你用到了十个功能模块，那你就需要导入十个。但是我们想让事情变得简单，一次导入，使用所有。

将所有的功能模块都进入到 `src` 的名称空间，在 `src/__init__.py` 里面我们设计成这样：

```python title="src/__init__.py"
from .cmdctl import CmdCtl
from .dogtails import Dogtail
from .find_image import FindImage
from .button_center import ButtonCenter


class Src(CmdCtl, FindImage):

    def __init__(self, **kwargs):
        """dogtail or button center param
        :param kwargs: app_name, desc, number
        """
        if kwargs:
            app_name = kwargs.get("APP_NAME")
            desc = kwargs.get("DESC")
            if app_name is None or desc is None:
                raise ValueError
            number = kwargs.get("number")
            number = number if isinstance(number, int) else -1
            # 对象组合
            self.dog = Dogtail(app_name, desc, number)
            self.ui = ButtonCenter(app_name, number)
```

需要传递参数的采用对象组合，没有参数的使用继承，继承的类符合 `Mixin` 设计模式。

应用库里面使用的时候在 `widget/base_widget.py` 里面只需要唯一继承 `Src` ：

```python title="widget/base_widget.py"
# 应用库里面方法基类
from src import Src

class BaseWidget(Src):
    """方法基类"""
    
    APP_NAME = "dde-file-manager"
    DESC = "/usr/bin/dde-file-manager"

    def __init__(self, number=-1):
        Src.__init__(self, APP_NAME=self.APP_NAME, DESC=self.DESC, number=number)
```

要使用核心库的功能，只需要写一个导入 `from src import Src` 即可。

写 `__init__` 构造函数的原因是通过参数构造应用，并且传递 `number` 进来，可以实现多窗口的控制。

### 3、==公共方法库（public）==

公共方法库里面每个应用都是一个单独的 `py` 文件，相互之间是独立的，每个 `py` 文件里面是该应用的方法类，比如：最常用的方法类 `dde_desktop_public_widget.py`

```python title="dde_desktop_public_widget.py" hl_lines="3 13"
from src import Src

class _DdeDesktopPublicBaseWidget(Src):
    """桌面公共方法基类"""
    
    APP_NAME = "dde-desktop"
    DESC = "/usr/bin/dde-desktop"

    def __init__(self):
        Src.__init__(self, APP_NAME=self.APP_NAME, DESC=self.DESC)
        
    
class DdeDesktopPublicWidget(_DdeDesktopPublicBaseWidget):
    """桌面公共方法类"""
    
    def click_music_dir_by_ui(self):
        """在文件选择框点击音乐目录"""
        self.click(*self.ui.btn_center("侧边栏-音乐"))   
    
    def click_xxx_by_attr(self):
        pass
```

==公共方法库意义==：

- 公共方法库里面所封装的一些操作方法都是至少被 2 个应用都用到的，这样做可以减少整体代码量，从而减轻应用库代码的维护工作。

- 公共方法库里面的编写形式（命名规则、定位的方案写法、注释的写法等等）具有一定的模板作用，这样即使是各个应用库都独立维护，所有的编码风格都是趋于相同的，因为大家都应该参照公共库里面的一些写法来写自己应用库里面的一些方法类，这样使得从公司的角度去看所有应用的自动化测试项目都是统一的。
- 可以通过公共方法库里面的一些方法，了解到其他应用的功能，对于我们需求理解，了解系统的方方面面也有好处。

当然，如果你的应用本身是属于根本就不需要和其他应用交互的，那么你可能不会用到这里面的功能，没关系，你所有的方法都可以直接写在应用库的业务层。

### 4、==conftest.py==

`conftest.py` 从功能上将是属于核心库（`src`）的内容，但是由于它的特殊性，即它是对应用库中的用例生效的，而且它的作用域是当前目录及以下，因此我们将它放到项目根目录。我们框架中有不少核心功能都是在这里面进行开发的，后面第四章会讲到细节。

`pytest.ini` 作用和 `conftest.py` 类似，是 `Pytest` 框架的固定配置文件，目前配置了一些通用的命令行执行参数，也放在项目根目录。

根目录下的 `conftest.py` 文件只会用来写 `Hook` 函数，`apps` 目录下的 的 `conftest.py` 文件只会用来写 `fixture` 。

### 5、==setting==

全局配置模块，包含了以下配置文件：

（1）`ini` 配置文件

主要配置一些全局的配置项，譬如：失败重跑次数、是否失败录屏、单条用例超时时间、会话超时时间、执行时日志级别、生成的报告类型、以及分布式执行的一些策略配置项等等。

（2）`config.py` 配置文件

主要提供配置文件读取、动态获取一些常量（如项目根目录绝对路径 `(BASE_DIR)`、系统架构（`SYS_FRAME`）、时间字符串（`strftime`）、本机 `USERNAME`  `IP` 等等）、公共 URL 等。

