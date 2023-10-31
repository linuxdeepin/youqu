# AT 开发规范

```shell
# ================================================
# Attribution : Chengdu Testing Department
# Time        : 2022/6/16
# Author      : mikigo
# ================================================
```

AT 开发规范是根据自动化测试运行两年多来，遇到问题解决问题而形成的一些解决方案，或者说经验总结；这些经验符合我们现阶段 AT 所应用的场景需要，也是我们经过长期思考，不断试错不断修正，并在自动化测试项目实践中检验过可行的。以此，希望能帮助参与到自动化的相关人员减少试错成本，更好、更快的编写用例及维护用例。

# 一、标签化管理规范

标签化管理文档请参考： [《用例标签化管理操作指引》](http://10.8.10.215/用例标签化管理操作指引.html) 

以下说几个容易出现的问题：

## 1. 对应关系

- 写完自动化用例之后，请在 `CSV` 文件中标记用例的 ID、等级。为了提醒标记，执行用例时在首行会输出 `ERROR` 日志： `CSV 文件里面没有对应的 ID`；

  在最终提交代码之前，你需要在 `CSV` 文件里面将ID、用例等级等标签补全，如果 `CSV` 文件里面没有对应 ID，后续在批量执行的时候，这些用例是不会执行的。

## 2. 名称一致

- `CSV` 文件的文件名、用例函数中间的名称一致、用例 `py` 文件中间的名称，这三个名称一致。

  举例：

  ```python
  # test_music_679537.py
  
  def test_music_679537():
      """用例标题"""
      pass
  ```

  那么 `CSV` 文件的名称为 `music.csv`。

  AT 框架底层代码实现是将 `CSV` 文件的名称与用例函数名称名称（`item.name`）进行对应，因此，注意 `CSV` 文件名称对应的是用例函数名称，即 `def test_music_001` 里面的 `music` ，而不是 `test_music_001.py` 里面的 `music` 。

  这里细细品一下哈~

  如果你将上例写成了这样:

  ```python
  # test_music_679537.py
  
  def test_movie_679537():
      """用例标题"""
      pass
  ```

  用例执行没问题，但是标签化管理是不生效的，框架无法将 `music.csv`文件里面标签，添加到 `test_movie_001`这个用例中，因为他们没有对应关系。

# 二、分支及 tag 管理规范

参考《[自动化测试代码管理规范](https://filewh.uniontech.com/lib/d01a57df-cba6-44f2-af8e-4cc412ad1880/file/01.%E4%BA%A7%E5%93%81%E5%BC%80%E5%8F%91%E4%BD%93%E7%B3%BB/02%20%E4%BA%A7%E5%93%81%E7%A0%94%E5%8F%91/01-3%20%E6%B5%8B%E8%AF%95%E8%BF%87%E7%A8%8B/%E8%87%AA%E5%8A%A8%E5%8C%96%E6%B5%8B%E8%AF%95/02-%E8%A7%84%E8%8C%83/%E8%87%AA%E5%8A%A8%E5%8C%96%E6%B5%8B%E8%AF%95%E4%BB%A3%E7%A0%81%E7%AE%A1%E7%90%86%E8%A7%84%E8%8C%83%20V2.0.pdf)》

## 2. 应用库 tag

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

## 3. 基础框架 tag

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

# 三、仓库权限管理

## 1. 基础框架

- 自动化测试基础框架仓库：https://github.com/linuxdeepin/deepin-autotest-framework


## 2. 应用仓库

- 自动化应用仓库：  `https://gerrit.uniontech.com/admin/repos/autotest_ +  app_name`

  链接后面的 `app_name` 中间以下划线连接，比如音乐：https://gerrit.uniontech.com/admin/repos/autotest_deepin_music


# 四、方法编写&调用规范

方法编写整体设计思路参考：[《AT应用库设计方案》]

## 1. 方法编写

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

## 2. 方法调用

- 在用例中调用方法，通过该应用唯一的出口进行调用，比如文管：

  ```python
  class DfmWidget(TitleWidget, RightViewWidget, LeftViewWidget, PopWidget):
      pass
  ```

  **不要在用例中单独去调用** `TitleWidget` 、`RightViewWidget`、`LeftViewWidget` 、`PopWidget` 这些类，否则后期用例会变得不好维护；

# 五、用例编写规范

## 1. 基于类写用例

所有用例都应该基于类去写：

```python
class TestMusic(BaseCase):
    """音乐用例"""
    
    def test_music_679537(self):
        """音乐启动"""
```

注意以下几点：

- 类名不要随便取，同一个应用应该使用同一个类名，用例类名称必须以 Test 开头，遵循大驼峰命名规范；

- 用例类继承 `BaseCase`，一个应用只有一个 `BaseCase`

- 一个 `py` 文件里面只有一个类，我们称为一个测试类；

- 一个类里面可以有多个用例函数，这取决这条用例有多少个测试点：

  ```python
  # test_music_679537.py
  
  class TestMusic(BaseCase):
      """音乐用例"""
      
      def test_music_679537_1(self):
          """任务栏启动音乐"""
          
      def test_music_679537_2(self):
          """启动器启动音乐"""    
          
      def test_music_679537_3(self):
          """桌面启动音乐"""
  ```

## 2. 用例函数规范

- 用例函数以 test 开头，遵循蛇形命名规范，中间为用例的模块名称，后面加用例 ID，最后加测试点序号，即 `test_${module}_${case_id}[_${index}]` ；

  比如：`test_music_679537_1`，index 从 1 开始。

- 函数功能说明里面写用例标题，直接复制 PMS 上用例标题即可，注意用三对双引号，不要用其他注释，更不要用井号注释写用例标题；

- 直接复制 `PMS` 用例

  用例步骤直接将 `PMS` 上用例步骤和预期复制进来，然后进行批量注释（`ctrl + /`），在注释的基础上去写用例脚本会更加方便全面，也比你自己写注释更节约时间：

  举例，`PMS` 用例：

![](https://pic.imgdb.cn/item/64f054c8661c6c8e54ff4c71.png)

  直接选中用例内容，复制下来，然后粘贴到自动化用例脚本中：

  ```python
  # test_music_679537.py
  
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

  ```python
  # test_music_679537.py
  
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

- 不写 `if __name__ == '__main__':`，不写多余的代码；

## 3. 数据驱动

- 如果用例操作步骤是相同的，只是一些参数变化，尽量使用数据驱动来实现用例；

- 如果你需要使用外部文件存放数据驱动的数据，不能因此引入依赖，尽量使用一些标准库能读取的文件格式，比如 `json、ini、CSV、xml、txt` 等文件格式；不建议使用 `Yaml、Excel、MySQL` 等数据格式；

- 读取数据时也尽量使用标准库去做，如使用 `pandas` 处理 `CSV` 就属于大材小用了，正常的数据驱动还没到需要大数据分析来处理的地步；

- 数据驱动的外部文件存放在 `widget/ddt/` 目录下；

- 数据驱动的写法：

  ```python
  @pytest.mark.parametrize("value", data)
  def test_smb_049(self, value):
  ```

  以上这种参数化的写法本身没什么问题，但是，这里必须要补充一个没有用的小知识：

  - 如果参数化数据里面的字符会原封不动的输出到 `item.name` 里面，显示非常不优雅，而且可以会引入一些意想不到的问题，可以感受一下：

    参数：

    ```python
    data = [
    "一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三", "qwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyui",  "12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678",
        ]
    ```

    现象是这样色儿的：

    ```shell
    test_smb_049.py::TestFileManager::test_smb_049[一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三]
    test_smb_049.py::TestFileManager::test_smb_049[qwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyuiopqwertyui]
    test_smb_049.py::TestFileManager::test_smb_049[12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678]
    ```

    说实话，看着心里堵得慌，如果这里面包含一些**特殊字符**或者是**超长**，可能会有一些很奇妙的事情发生。

  - parametrize 里面有个参数：ids，可以解决此类问题，就像这样：

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

## 4. 断言资源

- 用例断言的图片资源，直接放在用例模块的同级目录下的 `assert_res` 目录下，图片名称以用例的模块名称 + 用例 ID 命名；
- 图像识别断言，不要截取一张很大的图，图片资源包含的元素太多了，非常容易受到需求影响，建议是进行局部的断言；
- 图像识别的默认匹配度是 0.9，如果断言的场景对于精确度要求没那么高，可以在断言语句里面传入小于 0.9 的参数。

## 5. 元素定位

- 用于用例操作步骤中进行元素定位的图片资源，放到 `widget/pic_res` 目录下，图片名称命名为该元素的名称；
- 用于元素定位的图片截取时尽量精确到这个具体的按钮，图片也不要太大；
- 基于 UI 定位的操作较快，合理加入等待时间能提高用例的稳定性。

## 6. 用例资源

- 用例执行过程中需要使用到的一些资源，比如音乐可能需要一些 mp3 的资源用于测试，存放在 `widget/case_res` 目录下，前提是这些资源不超过 `10M`；

- 如果是一些比较大的资源，建议放到统一的 ftp 服务器 （ftp://10.8.10.245），需要执行用例的时候再下载下来；

  ```python
  f"wget ftp://{Config.FTP_IP}/uploads/多媒体/影院/auto/{file_name};unzip {file_name};rm -rf {file_name};"
  ```

- 测试资源下载到应用 `widget/case_res` 目录下；

- 禁止将测试资源存放在个人的机器上；

- 应该尽量保证，一个资源在一次用例执行中只需要下载一次，所以你不能每次使用的时候都去下载，这样可能会耗费大量的网络资源，而因为先判断本地是否存在此资源，如果不存在再去下载；

- 测试用例执行过程中，你可能需要将资源拷贝到对应的测试目录下，比如将 mp3 文件拷贝到 `~/Music` 目录下，但是我们更建议你使用发送快捷链接的方式替代拷贝的操作，因为在拷贝大文件时是很消耗系统资源的，而创建链接则不会；

  ```python
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

- 资源下载过程中注意超时的问题，如果你的测试资源很大，要特别注意这问题，如果你使用强制等待下载结束( `os.system` )，可能会造成用例执行时长变得不可接受，目前我们发现在持续集成环境执行时网络下载速度很慢，所以超时机制是很有必要的；`run_cmd` 方法有一个默认超时的时间，你可以根据资源大小对超时时间进行调整；

# 六、用例调试技巧

## 1. 日志

- 一定要先看报错，看 error 日志，通常能明确的告诉你具体哪里代码报错；
- 结合报错点前面的error、 info 和 debug 日志看否是正常。

## 2. 断点调试

- 方法报错：
  - 在方法库中找到对应的方法，单独调用，看是否能正常执行；
  - 通常单个方法的执行是比较简单的，如果单个方法报错，很快就能排查出问题；在方法内部打断点，使用 `Debug` 运行，看方法内部数据传递是否存在问题；
  - 如果单个方法调用没问题，那么在用例中报错的方法前面打断点，使用 `Debug` 运行，看用例的业务逻辑和数据传递是否存在问题；
- 断言报错：
  - 断言为数据断言，根据表达式进行断言语句进行修改；
  - 文件生成类断言，查看是否需要加等待时间；
  - 图像断言，在断言语句处打断点，使用 `Debug` 运行，用例运行到断言处会停止，查看此时断言的图片与用例执行的现场存在什么差异，此时也可以进行重新截图，从而替换新的图片；

## 3. 远程执行

- 远程执行指的是编辑器通过指定远程解释器执行自动化代码；

  远程执行的好处是可以很方便的 `Debug` 运行，不用在测试机上打开编辑器，用例执行速度更快；

  支持远程执行功能的编辑器：

  - 专业版 `Pycharm` 
  - `VScode` ，需要使用插件 `Remote-SSH`
  
- 远程执行配置

  以 `Pycharm` 为例：
  
  `File` —> `Settings` —> `Project` —> `Python Interpreter` —> `右边设置按钮` —> `Add...` —> `SSH Interpreter` —> `New server configuration(填入host和username)` —> `Next` —> `password（测试机密码）` —>  `Interpreter(选择远程解释器)` —> `Finish` 

## 4. 环境清理

- 如果用例里面的 `teardown` 没有执行，大概率是因为 `setup` 里面代码报错，这两个是一对的，`setup` 里面报错，`teardown` 里面的代码不会执行；
- 目前我们已经将各应用的 `clean_all` 这个 `fixture` 改成了终结器，确保始终能执行到这步，但是用例里面的 `fixture`，还是需要我们小心处理；
- 要执行 `clean_all` 需要在编辑器运行参数加 `--clean yes`，写用例的时候请加上，不然你不确定用例执行之后的环境是否恢复；
- `setup` 可以不要，将 `setup` 放到用例里面是一种稳妥的做法，`teardown` 一定要。

## 5. 元素定位不准（坐标返回不对）

- 基于 `UI` 定位的方法，可能受到窗口 ID 的变化，导致坐标返回不准，默认取最新的一个窗口用于定位，但如果实际需要定位的不是最新的窗口，那么在用例中需要重新实例化方法类对象，并在类中传入对应的窗口序号；
- 基于属性定位的方法，目前遇到的笔记本上，由于屏幕缩放比例为 1.25，导致坐标返回不准，我们默认使用缩放比例为 1；
- 基于图像定位的方法，如果当前屏幕中存在多个相同的目标元素，可能出现定位不准；支持通过参数控制，返回多个坐标；
- 基于 OCR 定位的方法，如果当前屏幕中存在多个相同的文字元素，可能出现定位不准；同样支持通过参数控制，返回多个坐标；

## 6. 键鼠操作不准

- 鼠标操作不生效，比如右键、双击无响应；
- 键盘操作不生效，或者延迟输入，比如用例需要输入“我是中国人”，实际只输入了“我国人”；

以上问题排除应用卡顿等问题，大概率是由于工具的问题，目前键鼠操作我们使用三个工具：`Dogtail` 提供的键鼠工具、`PyAutoGUI`、`Xdotool` ；

有同学可能要说为啥要用三个啊，用一个不就好了，简单讲就是各有优点各有缺点。

如果你遇到键鼠的问题，可以试试通过不同的工具操作；键盘输入延迟的问题，一般是因为输入速度太快了，系统没反应过来，常见于 `ARM` 和 `MIPS` 上，修改参数 delay_time 的值，单位为毫秒；

```python
# mouse_key.py

@classmethod
def input_message(cls, message, delay_time=300, interval=0.2):
    """
    输入字符串
    :param message: 输入的内容
    :param delay_time: 延迟时间
    :param interval:
    :return:
    """
```

如果不是方法的问题，则需要继续和开发一起排除，是否为应用接受键鼠信号处理的问题，这类情况我们也是遇到过的，具体问题具体分析。

比如影院就重写了一个右键的方法：

```python
# base_widget.py

@classmethod
def right_click(cls, _x=None, _y=None):
    """
    重写底层单击鼠标右键
    解决影院右键触发release事件的问题（右键主窗口会播放视频）
    """
    cls.mouse_down(_x, _y, button=3)
    sleep(0.1)
    cls.mouse_up(button=3)
```



# 七、其他不为人知的细节 

- 在一段时间内尽量编写同一个应用或模块的用例，能对该用例已有方法熟悉，避免过多重复业务代码的封装；
- 相同的场景下，各架构等待时间不同，建议使用框架提供的 sleep，我们做了不同架构的倍数放大；
- 编写用例时，尽量考虑到每一步异常后的环境恢复，需要建议这种意识，随时要考虑到，这步操作有没有可能出错，出错了改怎么办；
- 提交代码的时候注意不要把一些临时的测试资源提交进去了，比如测试了一个影片，有些同学习惯使用 `git add .` ，然后就全部提交到代码仓库了，这样即使后期把大文件删了，`.git` 文件里面也会很大，造成代码仓库变得十分臃肿。

更多细节查看：《AT经验总结》



