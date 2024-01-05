# AT 开发规范

```shell
# ================================================
# Author      : mikigo
# ================================================
```

AT 开发规范是根据自动化测试运行多年以来，遇到问题解决问题而形成的一些解决方案，或者说经验总结；

这些经验符合我们现阶段 AT 所应用的场景需要，也是我们经过长期思考，不断试错不断修正，并在自动化测试项目实践中检验过可行的。

以此，希望能帮助参与到自动化的相关人员减少试错成本，更好、更快的编写用例及维护用例。

## 1. 版本及依赖

基础框架会根据自身的功能开发进行版本迭代发布，==基础框架不与某个应用版本绑定==；

但是，==应用库会依赖于基础框架的版本==。因此，我们建议在==应用库==目录下保存一个文本文件用于记录所依赖的基础框架版本，类似于开发应用的 `debian/control` 文件的功能，为了保持统一，这个文件就命名为 `control`，放在应用库根目录下。

## 2. 命名规范

- ==用例 ID==

  每个应用自己维护一套 ID，可以是你自定义的 ID 值，也可以是用某些特有的 ID（比如 PMS 用例ID）；

  一个用例类里面有多个用例时，在用例名称后面加序号。

  ```python title="多用例函数命名"
  class TestFileManager(BaseCase):
      """文管用例"""
      
      def test_xxx_015_1(self):
          pass
      def test_xxx_015_2(self):
          pass
  ```




- ==方法函数命名==

???+ note "方法函数命名关键词列表"
    | 名称               | 单词                           |
    | :----------------- | :----------------------------- |
    | 左键点击           | click                          |
    | 右键点击           | right_click                    |
    | 双击               | double_click                   |
    | 移动               | move_to                        |
    | 拖动               | drag                           |
    | 新建               | new                            |
    | 拖动到             | drag_to                        |
    | 从哪里拖动到哪里   | drag_something_from_xxx_to_xxx |
    | 获取               | get                            |
    | 获取某个元素的坐标 | get_location                   |
    | 非特殊文件         | file                           |
    | word文件           | doc                            |
    | text文件           | text                           |
    | 文件夹             | dir                            |

- ==常量关键词命名==

???+ note "常量关键词列表"
    | 名称                           | 单词       |
    | :----------------------------- | :--------- |
    | 应用名称                       | `APP_NAME` |
    | 应用描述                       | `DESC`     |
    | 本应用以外的其他应用，比如帮助 | `HELP`     |

- ==方法层文件名==

???+ note "方法层文件名称列表"
    | 名称                         | 单词                                                         |
    | ---------------------------- | :----------------------------------------------------------- |
    | 方法包名                     | widget                                                       |
    | 方法文件名<br />（文管举例） | `dfm_widget.py`<br />`title_widget.py`<br />`right_view_widget.py`<br />`left_view_widget.py`<br />`pop_widget.py`<br />`base_widget.py`<br />`dfm_assert.py` |

- ==断言语句名称==

???+ note "断言语句命名规范"
    断言语句都是以 assert 开头

    | 断言                       | 语句                                                         |
    | :------------------------- | :----------------------------------------------------------- |
    | 判断文件是否存在           | assert_file_exists<br />assert_file_not_exists               |
    | 判断桌面目录下文件是否存在 | assert_file_exists_in_desktop<br />assert_file_not_exists_in_desktop |
    | 判断图片存在               | assert_image_exists<br />assert_image_not_exists             |
    | 判断影院中是否存在图片     | assert_image_exists_in_movie<br />assert_image_not_exists_in_movie |
    | 判断元素是否存在           | assert_element_exist<br />assert_element_not_exist           |
    | 判断是否相等               | assert_equal<br />assert_not_equal                           |
    | 判断是否为真               | assert_true<br />assert_false                                |

## 3. Fixture 规范

为统一编码风格方便后续用例代码维护，现做以下规范说明：

- 不建议使用 `Xunit` 的写法，统一采用 `Pytest` `fixture` 的写法。
- 应用内 `fixture` 谨慎使用 `autouse=True` ，非必要的情况下非常不建议使用这个参数。
- 调用 `fixture` 不能使用 `@pytest.mark.usefixture()`，使用直接在用例里面传入函数对象。
- 建议在一个 `conftest.py` 里面去写，一个应用也尽量维护一个 `conftest.py `文件。
- `fixture` 也需要写功能说明，函数名称要有具体含义。

## 4. 方法编写规范

- 方法类型使用逻辑：

  ```python
  if 没有用到实例对象：
  	if 没有用到类对象：
      	写静态方法，函数前加 @staticmethod
      else：
      	写类方法，函数前加 @classmethod
  else:
      直接写实例方法
  ```

  举例:

  ```python
  class TitleWidget:
      
      def click_xxx_by_ui(self):
      pass
  
      @staticmethod
      def click_xxx_by_ui():
          pass
  
      @classmethod
      def click_xxx_by_ui(cls):
          pass
  
  ```
  
- 函数名称不出现数字，需要表示数量的用单词表示。

- 函数功能注释。

  - 没有参数，没有返回

  ```python
  """点击某个元素"""
  ```

  - 有参数，没有返回

  ```python
  """点击某个元素
  arg1:xxx
  arg2:xxx
  """
  ```

  - 有参数，有返回

  ```python
  """点击某个元素
  arg1:xxx
  arg1:xxx
  return: xxx
  """
  ```

	用 `Pycharm` 的注释模板也可以，只要体现了参数的类型和返回就行了。

- 暂不要求写类型注解。

## 5. 用例编写规范

### 5.1. 基于类写用例

所有用例都应该基于类去写：

```python
class TestMusic(BaseCase):
    """音乐用例"""
    
    def test_music_679537(self):
        """音乐启动"""
```

注意以下几点：

- ==类名不要随便取==，同一个应用应该使用同一个类名，用例类名称必须以 Test 开头，遵循大驼峰命名规范；

- ==用例类继承 BaseCase==，一个应用只有一个 `BaseCase` ；

- ==一个 py 文件里面只有一个类==，我们称为一个测试类；

- ==一个类里面可以有多个用例函数==，这取决这条用例有多少个测试点：

```python title="test_music_679537.py"
class TestMusic(BaseCase):
    """音乐用例"""
    
    def test_music_679537_1(self):
        """任务栏启动音乐"""
        
    def test_music_679537_2(self):
        """启动器启动音乐"""    
        
    def test_music_679537_3(self):
        """桌面启动音乐"""
```



### 5.2. 用例函数规范

- 用例函数以 test 开头，遵循蛇形命名规范，中间为用例的模块名称，后面加用例 ID，最后加测试点序号，即：

  ```shell
  test_{module}_{case_id}[_{index}]
  ```

  比如：`test_music_679537_1`，`index` 从 1 开始。

- ==函数功能说明== 里面写用例标题，==直接复制 PMS 上用例标题即可==，注意用 ==三对双引号==；

- ==复制 `PMS` 用例步骤==

    直接将 `PMS` 上用例步骤和预期复制进来，然后进行批量注释（ ++ctrl+"/"++ ），在注释的基础上去写用例脚本会更加方便全面，也比你自己写注释更节约时间：

    举例：
	???+ note "PMS用例"
    	![](https://pic.imgdb.cn/item/64f054c8661c6c8e54ff4c71.png)

    直接选中用例内容，复制下来，然后粘贴到自动化用例脚本中：

    ```python title="test_music_679537.py"
    class TestMusic(BaseCase):
    """音乐用例"""
    
    def test_music_679537(self):
        """演唱者-平铺视图下进入演唱者详情页"""
    
        # 1
        # 点击右上角的【平铺视图】按钮
        # 切换为平铺视图
        # 2
        # 双击任意演唱者封面
        # 进入演唱者详情页面
    ```
    
    上例中井号注释部分就是直接从 `PMS` 上复制过来的，在此基础上写用例：
    
    ```python title="test_music_679537.py"
    class TestMusic(BaseCase):
    """音乐用例"""
    
    def test_music_679537(self):
        """演唱者-平铺视图下进入演唱者详情页"""
        music = DeepinMusicWidget()
        music.click_singer_btn_in_music_by_ui()
        # 1
        # 点击右上角的【平铺视图】按钮
        music.click_icon_mode_in_music_by_ui()
        # 切换为平铺视图
        # 2
        # 双击任意演唱者封面
        music.double_click_first_singer_in_singer_icon_view_by_ui()
        # 进入演唱者详情页面
        self.assert_xxx
    ```
    
    你看，非常清楚每一步在做什么，重点是省去了写注释的时间，真的炒鸡方便。


### 5.3. 数据驱动

- 如果用例操作步骤是相同的，只是一些参数变化，尽量使用数据驱动来实现用例；

- 如果你需要使用外部文件 ==存放数据== 驱动的数据，==尽量不要因此引入依赖==，可以使用一些标准库能读取的文件格式，比如 `json、ini、CSV、xml、txt` 等文件格式；==不建议== 使用 `Yaml、Excel、MySQL` 等数据格式；

- ==读取数据== 时也尽量使用标准库去做，如使用 `pandas` 处理 `CSV` 就属于大材小用了，正常的数据驱动还没到需要大数据分析来处理的地步；

- 数据驱动的外部文件存放在 ==widget/ddt/== 目录下；

- 数据驱动的写法：

  ```python
  @pytest.mark.parametrize("value", data)
  def test_smb_049(self, value):
  ```

  以上这种参数化的写法本身没什么问题，但是，这里必须要补充一个没有用的小知识：

  - 如果参数化数据里面的字符会原封不动的输出到 `item.name` 里面，显示非常不优雅，而且可能会引入一些意想不到的问题，可以感受一下：

    参数：

    ```python
    data = [
    	"一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三",
    	"qwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyui", 
    	"12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678",
        ]
    ```

    终端日志打印出来，现象是这样色儿的：

    ```shell
    test_smb_049.py::TestFileManager::test_smb_049[一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三]
    test_smb_049.py::TestFileManager::test_smb_049[qwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyui]
    test_smb_049.py::TestFileManager::test_smb_049[12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678]
    ```

    说实话，看着心里堵得慌，如果这里面包含一些**特殊字符**或者是**超长**，可能还会有一些很奇妙的事情发生。

  - parametrize 里面有个参数：==ids==，可以解决此类问题，就像这样：

    ```python
    @pytest.mark.parametrize("value", data, ids=[1, 2, 3])
    def test_smb_049(self, value):
    ```

    再来感受一下：

    ```shell
    test_smb_049.py::TestFileManager::test_smb_049[1]
    test_smb_049.py::TestFileManager::test_smb_049[2]
    test_smb_049.py::TestFileManager::test_smb_049[3]
    ```

    明显好多了，所以尽量使用 ids 这个参数。

- 不建议使用 `fixture` 的数据驱动方式，框架虽然支持，但可读性比较差；如果你不知道这句话在说啥，那你可以忽略，我也不打算详细说这种实现方式，操作比较骚。

### 5.4. 断言资源

- ==用例断言的图片资源==，直接放在 ==用例模块的同级目录下的 assert_res 目录== 下，图片名称以 ==用例的模块名称 + 用例 ID 命名==；
- 图像识别断言，不要截取一张很大的图，图片资源包含的元素太多了，非常容易受到需求影响，建议是进行局部的断言；

### 5.5. 元素定位

- 用于 ==用例操作步骤中进行元素定位的图片资源==，放到 ==widget/pic_res 目录== 下，图片名称命名为该元素的名称；
- 用于元素定位的图片截取时尽量精确到这个具体的按钮，图片也不要太大；
- 基于 UI 定位的操作较快，合理加入等待时间能提高用例的稳定性。

### 5.6. 用例资源

- 用例执行过程中需要使用到的一些资源，==存放在 widget/case_res 目录== 下，前提是这些资源不超过 ==10M==；

- 如果是一些比较大的资源，建议放到统一的 ftp 服务器，需要执行用例的时候再下载下来；

- ==确保一个资源在一次用例执行中只需要下载一次==，如果每次使用的时候都去下载，这样可能会耗费大量的网络资源，而因为先判断本地是否存在此资源，如果不存在再去下载；

- 测试用例执行过程中，你可能需要将资源拷贝到对应的测试目录下，比如将 mp3 文件拷贝到 `~/Music` 目录下，但是我们更建议你使用发送快捷链接的方式替代拷贝的操作，因为在拷贝大文件时是很消耗系统资源的，而创建链接则不会；

  ```python
  class DeepinMusicWidget:	
  
      @classmethod
      def recovery_many_movies_in_movie_by_cmd(cls):
          """恢复多个视频文件至视频目录中"""
          work_path = f"/home/{Config.USERNAME}/Videos/auto"
          code_path = f"{Config.CASE_RES_PATH}/auto"
          cls.run_cmd(f"rm -rf {work_path};mkdir {work_path}")
          sleep(1)
          flag = False
          if not exists(code_path):
              cls.run_cmd(f"mkdir -p {code_path}")
              flag = True
          logger.info(f"ln -s {code_path}/* {work_path}/")
          cls.run_cmd(
              f"cd {code_path}/;"
              f"{cls.wget_file('auto.zip') if flag else ''}"
              f"ln -s {code_path}/* {work_path}/ > /dev/null 2>&1"
          )
  ```

  资源下载过程中注意超时的问题，如果你的测试资源很大，要特别注意这问题，如果你使用强制等待下载结束( `os.system` )，可能会造成用例执行时长变得不可接受，目前我们发现在持续集成环境执行时网络下载速度很慢，所以超时机制是很有必要的；`run_cmd` 方法有一个默认超时的时间，你可以根据资源大小对超时时间进行调整；



## 6. 标签化管理规范

### 6.1. 对应关系

写完自动化用例之后，请在 `CSV` 文件中标记用例的 ID、等级等标签。

为了提醒标记，执行用例时在首行会输出 `ERROR` 日志： `CSV 文件里面没有对应的 ID`；

如果 `CSV` 文件里面没有对应 ID，后续在批量执行的时候，这些用例是不会执行的。

### 6.2. 名称一致

==CSV 文件的文件名==、==用例 py 文件中间的名称==、==用例函数中间的名称==，这三个名称一致。

举例：

```python title="test_music_679537.py"
class TestMusic:
    
    def test_music_679537():
        """用例标题"""
```

那么 `CSV` 文件的名称为 ==music.csv==。

框架底层代码实现是将 ==CSV 文件的名称== 与 ==用例脚本名称== 进行对应（建立映射）；



## 二、分支及 tag 管理规范

参考《[自动化测试代码管理规范](https://filewh.uniontech.com/lib/d01a57df-cba6-44f2-af8e-4cc412ad1880/file/01.%E4%BA%A7%E5%93%81%E5%BC%80%E5%8F%91%E4%BD%93%E7%B3%BB/02%20%E4%BA%A7%E5%93%81%E7%A0%94%E5%8F%91/01-3%20%E6%B5%8B%E8%AF%95%E8%BF%87%E7%A8%8B/%E8%87%AA%E5%8A%A8%E5%8C%96%E6%B5%8B%E8%AF%95/02-%E8%A7%84%E8%8C%83/%E8%87%AA%E5%8A%A8%E5%8C%96%E6%B5%8B%E8%AF%95%E4%BB%A3%E7%A0%81%E7%AE%A1%E7%90%86%E8%A7%84%E8%8C%83%20V2.0.pdf)》

### 2. 应用库 tag

- 应用库 tag 根据应用交付节点生成，每次打 tag 之前，相关测试人员需要进行用例调试；

- 调试用例是指的在全架构（x86、arm、mips）上调试通过；

- 用例通过率达到 **90%** 以上才能打 tag，通过 Jenkins 执行器执行用例，保留通过率结果；

  - 用例通过率：通过用例数 / (总用例数 - 已废弃用例)    *跳过的用例不算通过* 
  - [Jenkins 执行器](https://jenkinswh.uniontech.com/view/CI/job/chengdu/job/AT_test/job/all_client_test/)

- 你可能会在一个交付周期内持续的进行AT用例调试，但是最终 AT 用例打 tag 的应用版本，**需要使用应用集成交付的最新应用版本**，可以使用应用的提测版本；一定要确保调试用例的应用版本是最新的，不然集成进去之后，持续集成就会出问题；

- tag 号怎么打？

  根据持续集成的要求生成，其中应用版本号需要与项目经理确认本次即将集成的应用版本号是多少；

  tag 的 commit 信息格式：

  ```ini
  # commit msg
  version:5.6.5
  ```

  其中 `5.6.5` 写应用的集成版本号。

生成 tag 的命令参考：[《Git 标签》](http://10.8.10.215/README.html#git )

### 3. 基础框架 tag

基础框架 tag 不与业务挂钩，根据自身的功能开发按需发布版本，在根目录下 `CURRENT` 文件中记录的当前版本号和历史版本号，及其对应新增了哪些功能，有助于应用选择合适的基础框架版本。

```ini
# CURRENT
[current]
tag = 0.9.5
```

应用库根目录下的 `control` 文件记录当前应用库依赖的基础库版本。

```ini
# control
[Depends]
autotest-basic-frame = 0.9.5
```

用例在执行时会校验两个文件的版本号是否一致，如果不一致，会打印 `error` 日志。

## 三、仓库权限管理

### 1. 基础框架

- 自动化测试基础框架仓库：https://github.com/linuxdeepin/deepin-autotest-framework


### 2. 应用仓库

- 自动化应用仓库：  `https://gerrit.uniontech.com/admin/repos/autotest_ +  app_name`

  链接后面的 `app_name` 中间以下划线连接，比如音乐：https://gerrit.uniontech.com/admin/repos/autotest_deepin_music


## 四、方法编写&调用规范

方法编写整体设计思路参考：[《AT应用库设计方案》]

### 1. 方法编写

写方法的时候注意方法归属，比如文件管理器的界面区域划分为：`TitleWidget` 、`RightViewWidget`、`LeftViewWidget` 、`PopWidget`，方法是在哪个区域操作的，就写在哪个类里面。

举例：

```python
from apps.dde_file_manager.widget import BaseWidget  # dde_file_manager 为仓库名称

class TitleWidget(BaseWidget):
    """标题栏方法类"""

    def click_xxx_in_title_by_ui(self):
        """点击标题栏xxx"""
        # self.dog.find_element_by_attr("xxxx").click()
        self.click(*self.ui.btn_center("xxx"))
```

- 动作开头，注意是动词

  ```asciiarmor
  click
  double_click
  right_click
  get
  make
  ```

- 元素对象名称

  - 界面元素直接与元素名称相同，没有名称的就取一个好听易懂的名字。

- **加上类的关键词**

  - 避免方法重名，同时可以标记区域。

- 标定操作方法

  ```asciiarmor
  by_ui
  by_attr
  by_mk
  by_img
  ```

### 2. 方法调用

- 在用例中调用方法，通过该应用唯一的出口进行调用，比如文管：

  ```python
  class DfmWidget(TitleWidget, RightViewWidget, LeftViewWidget, PopWidget):
      pass
  ```

  **不要在用例中单独去调用** `TitleWidget` 、`RightViewWidget`、`LeftViewWidget` 、`PopWidget` 这些类，否则后期用例会变得不好维护；

## 其他规范

- 不写 `if __name__ == '__main__':`，不写多余的代码；
- 统一文件注释头。

  ```python
  #!/usr/bin/env python3
  # _*_ coding:utf-8 _*_
  """
  :Author:email@uniontech.com
  :Date  :${DATE} ${TIME}
  """
  ```
- 日志打印要在方法最前面，否则代码报错没有日志输出，不好定位问题。（我们会考虑继续使用拦截器打印日志）
  
  - 所有的操作都需要有日志，包括 `sleep()`，我们会重写一个有日志输入的 `sleep`。
  - 业务层日志级别为 `INFO`。
- hook 函数只能写到根目录下的 `conftest.py` 里面。
- `apps` 目录下的 `conftest.py` 原则上不会新增 `fixture`。
- 固定目录或元素控件的操作，将操作方法写死，文件类操作将文件名留参数。
- 路径拼接规范：
  - 系统中固定目录，路径拼接时使用波浪符号，比如：`~/Desktop/`，下层使用 `os.path.expanduser()`，它可以自动识别波浪符号。
  - 项目下路径使用配置文件中的路径，比如：`Config.BASE_PATH`，因为项目是可以在任意路径运行的，需要动态拼接路径。







