# AT 经验总结

> 欢迎所有人提交你在自动化测试方面的优秀实践经验，以帮助大家解决可能遇到的问题。

# 1、终结器

```shell
# litaoa@uniontech.com
```

前置/后置步骤

pytest 实现前置/后置步骤的方式有两种，yield 和终结函数；

yield 实现，yield前面为用例的前置步骤，yield 后面为用例的后置步骤。

```python
@pytest.fixture
def clean_env():
    print("setup")
    yield
    print("teardown")
```

终结函数实现，使用 request.addfinalizer 注册用例的后置步骤

```python
@pytest.fixture
def clean_env(request):
    def clean():
        print("teardown")
    request.addfinalizer(clean)
    print("setup")
```

yield的优缺点：

优点：代码简洁，直观，可使用yield在用例中获取前置步骤的返回值

缺点：若前置步骤中出现错误，则后置步骤不会执行

终结函数：

优点：前置步骤失败的话，后置步骤仍会执行且可以注册多个后置步骤（前提：需要在代码报错之前注册后置步骤），支持灵活使用后置条件

缺点：代码较为复杂，无法获取前置步骤的返回值（本人目前未实现）

总结：在前置步骤保证绝对不会出错时，使用yield更佳简便，当前置步骤易出现问题时，推荐使用终结函数。

场景：保险箱用例，前置步骤中开启保险箱，后置步骤删除保险箱。

```python
@pytest.fixture(scope="session", autouse=True)
def vault_fixture(request):
    DfmWidget.reset_vault_by_cmd()	# 1、重置保险箱
    DdeDockPublicWidget().close_file_manager_by_cmd() # 2、关闭文管
    DdeDockPublicWidget().open_file_manager_in_dock_by_attr() # 3、开启文管
    vault = DfmWidget()
    vault.create_file_vault()	# 4、创建保险箱

    def delete_vault():	# 8、删除保险箱的后置步骤
        sleep(2)
        DdeDockPublicWidget().open_file_manager_in_dock_by_attr()
        vault = DfmWidget()
        vault.delete_file_vault()
        DfmWidget.reset_vault_by_cmd()
        DdeDockPublicWidget().close_file_manager_by_cmd()
    request.addfinalizer(delete_vault)	# 5、注册后置步骤
    DdeDockPublicWidget().close_file_manager_by_cmd()	# 6、关闭文管
    sleep(1)
    DdeDockPublicWidget().open_file_manager_in_dock_by_attr() # 7、开启文管
```

代码按注释中的序号执行步骤

- 代码在步骤1-4任意位置报错，则不会执行步骤8，因为未执行到步骤5，步骤8还未注册
- 代码在步骤6-7报错，仍会执行步骤7，因为在步骤5中已经将步骤7注册

可以灵活注册后置步骤，能实现某个前置步骤执行之后，才会执行后置步骤。

# 2、启动应用的方式

```shell
# huangmingqiang@uniontech.com
```

（1）命令行启动

在 AT 代码中使用命令行启动应用，举例：

```python
os.popen("deepin-music")
```

这种方式启动存在一个问题，就是当使用 ssh 远程执行用例时，`dogtail` 无法获取到元素。

（2）通过 UI 操作启动

通过任务栏、启动器、桌面等UI方式启动，比如双击打开、右键打开等，这种操作方式不存在ssh 远程执行用例时`dogtail` 无法获取到元素的问题，也更加符合用户的操作行为。

# 3、文件选择框属性定位偶现无法找到
文件选择框存在一个问题，在调用文件选择框时，有一定的概率出现，界面已经渲染出来了，但是属性树并没有写入，导致通过属性无法找到元素，目前也没有很好的解决方案，为了用例稳定性，文件选择框的操作建议使用UI或者图片定位的方式，可以通过搜索内容固定文件位置。

```shell
# litaoa@uniontech.com
```

```python
desk = DdeDesktopPublicWidget()
# 选择视频目录
desk.click_videos_dir_in_desktop_plugs_by_ui()
sleep(1)
desk.ctrl_f()
sleep(1)
desk.input_message("元素名称")
sleep(0.5)
desk.enter()
sleep(1)
# 选择第一个文件
desk.click_list_view_btn_in_desktop_plugs_by_ui()
sleep(1)
desk.click_first_file_in_desktop_plugs_by_ui()
sleep(1)
# 文管插件中点击打开
desk.click_open_btn_in_desktop_plugs_by_ui()
```

# 4、应用启动

```shell
# mikigo
```

在UI自动化测试中，一切操作的都是从应用启动开始的，而在Linux桌面应用自动化测试中，我们启动应用的方法有多种，下面做一个简单的介绍：

**【使用dogtail启动】**

dogtail提供了应用启动的方法，在utils库中，使用run方法启动：

首先导入方法：

```python
from dogtail.utils import *
```

调用run方法

```python
run('deepin-music')
```

即可启动音乐
![img](https://img2020.cnblogs.com/blog/1898113/202012/1898113-20201218162414410-1539488857.png)

这种方法的优点是采用进程的方式直接启动，不依赖与UI，无论桌面或任务栏上是否存在应用图标，都可以正常启动。

但是在实际项目中，仍然存在一个问题，

如果使用ssh远程调用，或者Jenkins中执行测试脚本的时候，在sniff中会出现找不到应用，经过分析，可能是因为使用这种方法启动的时候，实际是采用一个子进程启动了应用，dogtail无法识别到。

**【从任务栏启动】**

使用dogtail点击任务栏上的应用图标

通常有两种方法：

（1）使用dogtail点击任务栏上的应用图标。

（2）已知应用图标在任务栏上的位置，然后使用鼠标点击对应坐标。

第二种方法的缺点是位置必须固定，如果移动位置就不行了，而使用第一种方法，无论位置在哪里，只要图标在任务栏上存在即可。

**【点击桌面图标启动】**

桌面图标目前是采用图像识别技术，定位到应用图标的坐标，然后通过pyauogui进行点击操作。

详细技术方案可以参考我的另外两篇博客:

[基于opencv的模板匹配实现图像识别，返回在屏幕中的坐标](https://www.cnblogs.com/mikigo/p/13489143.html)

[Python三方库PyAutoGui的使用方法](https://www.cnblogs.com/mikigo/p/13182619.html)

**【从启动器启动（俗称开始菜单）】**

启动中启动的实现逻辑实际和任务栏上启动差不多。

首先，需要使用鼠标点击任务栏上的启动器图标，或者键盘super键，将启动器呼出来，

然后，在启动器中点击对应的图标，

但是这里有个问题，启动器中的应用列表，一页展示不完，所以如果我们要点击的应用图标不在第一页怎么办，通常解决方案有两种：

（1）需要进行向下滑动，这里就涉及到相应的识别方案，判断如果不在第一页就往下滑动翻页。

（2）启动器提供搜索的功能，输入应用名称搜索，然后进行点击。

从实际操作中来看，采用第二种方法的效率会高一点。

**【终端命令启动】**

在python中，使用os.popen()或os.system()或者subprocess.Popen()，实现命令行启动，比如：

```python
import os
os.popen('deepin-music')
```

这种方式启动是比较简单的，但是在实际项目中，仍然存在远程执行脚本的时候，dogtail无法识别的问题。

**【总结】**

以上几种方法，各有优缺点，在实际项目中：

（1）如果需要在Jenkins中做持续集成，建议使用第二种任务栏启动的方法。

（2）如果不会采用远程执行的，建议采用第一种或者最后一种方案。

（3）第三种和第四种启动方法，通常在测试用例中会涉及到，所以偶尔会用。