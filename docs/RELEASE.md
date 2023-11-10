# 版本更新记录

## 2.3.2（unreleased）

**New**

- 由于 `PMS` 用例管理系统存在缺陷，框架移除从 `CSV` 反向同步标签到 `PMS` 功能；

**Fix**

- 优化数据回填逻辑，修复同一个用例 `py` 包含多个用例，数据回填时，中间的失败结果被后续用例更新为的问题；

## 2.3.1（2023/11/8）

**New**

- 集成 `ydotool` 键鼠控制方案，解决锁屏界面控制键鼠的问题；

**Fix**

- 修复 `PMS` 回填数据时，`timeout` 报错的问题；
- 修复反向同步标签，导致 `PMS` 产品库用例 `title` 为空的问题；

## 2.3.0（2023/10/27）

**New**

- 增加了 `YouQu` 最新版本的检查，如果本地执行版本不是最新的，会打印更新提示信息；
- `public` 独立发布，基础框架移除此模块，在环境部署阶段进行 `public` 模块的初始化；

**Fix**

- 修复 `youqu` 命令无法接收带空格的参数的问题；感谢 **[@禄烨](https://github.com/lu-xianseng)** ；
- `OCR` 检测模型升级到 `V4` 之后，在识别某些文本情况下出现不能识别的问题，暂时先回滚到 `V3` ；
- 修复了不同的 `case` 目录下 `py` 文件的名称一样，导出（`manage.py csvctl -p2c`）数据错误的问题；感谢 **@赵有志**；

-----------------------

## 2.2.4（2023/10/16）

**New**

- `OCR` 检测模型升级到 `V4` ，中英文场景检测模型准确率提升 4.9%，识别模型准确率提升 2%；

- 支持标签反向同步：将 `csv` 中的标签同步到 `pms` ； 

- 解除子项目的工程名称以 `autotest_` 开头的限制，子项目工程名称可以为任意名称；

    配置文件 `globalconfig.ini` 中的 `APP_NAME` 和命令行参数 `-a/--app` 仅支持传入工程名称的全称：

    ```shell
    youqu manage.py run -a apps/autotest_deepin_music
    # 或
    youqu manage.py run -a autotest_deepin_music
    ```

- 新增导入全局配置对象：

    ```python
    from setting import conf
    ```

    这种写法和之前的写法效果是一样的；

    ```python
    from setting.globalconfig import GlobalConfig
    ```

- 继续尝试将一些功能模块拆分为独立构件；

- 增加了在线文档的显示宽度；

- 增加执行前显示执行的Python文件数量

**Fix**

- 修复从 `pms` 标签【设备类型】为 `null` 时，同步到 `csv` 文件写入为 `null`；
- 修复无法导出 `csv` 文件的问题；
- 修复了键盘 `printscreen` 按钮无效的问题； 
- 修复了 `sniff` 命令报错无法找到 `src` 模块的问题；
- 修复 `assert_ocr_not_exist` 传入多个识别目标逻辑判断错误的问题；

--------------------------

## 2.2.3（2023/9/15）

**New**

- 尝试将一些功能模块拆分为独立构件；

**Fix**

- 修复了远程执行传入 `app_name` 无法收集到用例的问题； 
- 优化了 `docs` 文档内容及排版；

-----------------------------

## 2.2.1（2023/9/13）

new

- 新增用例脚本 `py` 文件 `id` 自动同步到 `csv` 文件功能；
- 新增自动从 `pms` 上获取用例相关标签的功能；

fix

- 修复了 `letmego` 在开发调试时也会记录执行过程的问题；
- 优化了在线文档内容和排版；

----------------------------------

## 2.2.0（2023/9/5）

new

- 正式启用 `letmego` 技术方案；

fix

- 对 `docs` 里面细化了远程执行章节的描述；
- 多 `docs` 里面优化了标签化管理章节的描述；

## 2.1.5（2023/8/31）

new

- 将有趣的文档系统迁移到 [linuxdeepin](https://github.com/linuxdeepin/deepin-autotest-framework) ，剥离文档中的图片资源，采用 `CDN` 网络加速方式加载；

- 尝试合入一个有趣的功能；

fix

- 修复了 Wayland 键鼠工具没有鼠标相对移动方法 moveRel 的问题； 
- 修复了 Wayland 下获取窗口信息功能模块中环境变量的问题；
- 优化了 startproject 功能的一些信息输出；
- 修复了特殊场景下 env_dev.sh 开发环境部署是可能影响到正式环境 env.sh 的问题；

## 2.1.2（2023/8/22）

new

- 增加 OCR 识别自动重试机制，默认重试 2 次，支持动态传入重试次数；
- 使用窗管最新提供的二进制接口，优化基于 `UI` 的元素定位方案在 `Wayland` 下获取窗口信息的方法；感谢桌面测试部 **@何权 @孙翠** 、窗管研发 **@黄泽铭** 的大力支持。
- 扩充 `skipif` 条件跳过的功能函数：
  - `skipif_xdg_type` 支持 `x11` 或 `wayland` 上跳过；
  - `skipif_cpu_name` 支持不同 `cpu` 上跳过，比如：`skipif_cpu_name-KLVVW5821`；


## 2.1.0（2023/8/18）

fix

- 修复 SW 架构环境依赖的问题，原因是之前我这里本地没有 SW 的机器，没有做相关适配；

- 修复子项目单独需要三方包 `pexpect`，由于之前是预装到镜像里面的，但基础框架不需要，因此没有装载到虚拟环境里面，导致子项目依赖报错。

- 修复子项目 cv 导入报错的问题；

    原因为：youqu 的图像识别功能兼容两种情况，一种是面向服务，就是本地测试机不需要安装 `OpenCV`，用例中的图像识别会通过远程服务接口进行图像识别和结果获取；第二种是原生，就是本地直接安装 `OpenCV` 直接用。两个情况的优先级是优先判断本地存在，否则走服务。

    前面我们已经把 OCR 功能做了服务化，基于 1 年多以来的观察，用起来很稳定，再一个就是 `OpenCV` 安装包是比较臃肿的，粗略数了下依赖有 `30+` 个，而且在各架构上依赖包还不尽相同，装载到虚拟环境方案中不太好处理，所以本次 2.0 版本我们大胆的将图像识别的默认功能修改为面向服务的方式，前期测试一切看起来都很和谐。

    但是没注意到之前给海燕姐那边项目单独定制做了个图像识别接口（为了能简单平滑的迁移到 youqu），此接口底层没有兼容服务化，所以她那边的项目调用此定制接口会报 cv 导入的问题。

    由于将这个定制图像识别接口进行服务化兼容改造需要一定时间，改完还需要测试，但本次时间比较紧，因此先把 `OpenCV` 装进虚拟环境，后续版本再考虑针对此接口做修改。

## 2.0.0（2023/8/16）

`YouQu`（自动化测试基础框架）开源了，同时推出了 2.0 版本。

感谢**王波总、架构师徐小东、研发经理郑幼戈、刘郑**等研发同事的大力支持。

new

**1、新的基础框架代码获取方式及新的初始化工程命令**

`YouQu` 后续均通过 `PyPI` 进行包的发布，也就是说后续可以使用 pip 进行安装：

```sh
sudo pip3 install youqu==2.0.0
```

这里有 2 个小点要注意：

- 推荐使用 `sudo pip3` （加 sudo）进行安装；

    如果不加 sudo 有些机器可能 `$HOME/.local/bin` 不在系统 PATH 环境目录下，在不添加环境变量的情况下，会出现 `YouQu` 的初始化工程命令（youqu-startproject）无法使用的问题；

    当然，将上述路径添加到环境变量之后也是可以用的，所以我这里是推荐加 sudo，不加 sudo 也是可以的，只是需要关注下环境变量的问题。

- 推荐指定版本号（`youqu==2.0.0`）安装，如果不指定版本号默认是安装最新发布的 YouQu 版本，你可以在 [PyPI](https://pypi.org/project/youqu/) 上的 Release history 里面查看有哪些版本。

    安装之后会自动生成一个系统命令 youqu-startproject，使用它可以初始化工程，这里以音乐举例；

    ```shell
    youqu-startproject autotest_deepin_music
    ```

    这样就会在当前目录下生成一个 `autotest_deepin_music` 目录，里面包含了基础框架所有的代码；

    之后，还是在 `apps` 目录下，放入子项目的AT代码即可，使用方法和过去一样，这里就不多介绍。

    另外，除了通过 pip 获取以外，仍然可以通过源码获取（直接 git clone）。

    值得一提的是，使用 pip 安装 `YouQu` 时，`YouQu` 包的大小才 `600+` k，安装速度起飞。

**2、新的AT虚拟化环境部署方案**

为了解决以下问题：

- 过去一段时间咱们经常出现的，不同的AT项目在同一台机器上部署环境时依赖版本冲突的问题，新方案不同的项目会动态生成自己的虚拟环境，相互之间不影响；
- 业内为了解决版本冲突问题一般都会使用 `Python` 虚拟环境的工具，但是都有个问题，无法管理 deb 包形式发布的 Python 包，本次我们解决了这个问题，能够完全管理常规的 `Python` 包，也能管理到 deb 包形式发布的 Python 三方包；

    虚拟化环境部署使用方法：

    ```shell
    bash env.sh
    ```

    可以看出来和原来使用方法没有变化，也就是说从使用的角度是完全没有区别的，只是内部做了不同的事情。

    值得一提的是，本机部署的功能仍然保留 `env_dev.sh`，可以作为开发时的环境部署。

**3、新的驱动命令**

过去咱们都是使用这样的命令来驱动执行：

```shell
python3 manage.py run
```

由于默认基于虚拟化环境部署方案，因此我们增加了一个系统命令 `youqu`；

**新的驱动方式：**

```shell
youqu manage.py run
```

只需要把 python3 替换成 youqu 就可以了，看起来很和谐~

**4、新的文档地址**

过去咱们 `YouQu` 的在线文档是部署在公司内网的，现在开源到 github 了，外部开发者肯定访问不到内网的文档，因此需要将文档部署到公网【[公网文档](https://linuxdeepin.github.io/deepin-autotest-framework/)】；

公网文档使用的是 github pages（白嫖怪一顿狂喜~~），但可能会出现文档速度慢的问题（代理下就好了），不过没关系，咱们【[内网文档](http://youqu-dev.uniontech.com/)】仍然保留，文档内容一样，访问速度更快。

**5、其他一些小小功能更新：**

（1）新增关闭分辨率检测的参数值；

```sh
youqu manage.py run --resolution no
```

或者修改 `setting/globalconfig.ini` 里面的配置：

```ini
;检查测试机分辨率, 比如：1920x1080
;no: 表示不做分辨率校验
RESOLUTION = 1920x1080
```

`resolution` 这个参数一直都有的，只不过之前是用于指定分辨率大小，比如 `--resolution 1920x1080`，但有些接口的项目不需要这个检查，可以给它个 no 就好了，当然 CICD 上关闭，需要流水线上把这个参数加上；

（2）新增失败录屏从第几次失败开始录制视频的命令行参数

之前这个配置项只能在 `setting/globalconfig.ini` 里面的配置：

```ini
;失败录屏从第几次失败开始录制视频。
;比如 RECORD_FAILED_CASE = 1 ，表示用例第 1 次执行失败之后开始录屏，RERUN >= RECORD_FAILED_CASE。
;1.关闭录屏：RECORD_FAILED_CASE > RERUN
;2.每条用例都录屏：RECORD_FAILED_CASE = 0
RECORD_FAILED_CASE = 1
```

现在将开发到命令行参数。

```sh
youqu manage.py run --record_failed_case 2
```

fix

- 修复 `remote` 执行时，在某些情况下无法生成测试报告的问题；

## 1.3.0（2023/7/10）

fix 

- 进一步优化了 `env.sh` 安装 `Python` 的三方源；参考：[配置Python源的几种方法](https://funny-dream.github.io/funny-docs/Python/配置Python源的几种方法/)
- 修复 `wayland_autotool` 受安全管控的问题；
- 修复了`wayland`下偶现找不到 `.Xauthority` 文件的问题； 

## 1.2.9（2023/6/26）

fix

- 优化远程执行 `remote` 的参数直接传给远程机器的 `run` 命令，不用再单独处理远程执行的参数逻辑，后续专注于本地执行功能开发，远程执行自动适用；

- `env.sh` 移除 `pyyaml` 安装，由子项目在 `requirement.txt` 里面定义，框架自动加载；

- 优化了 `env.sh` 安装 `Python` 的三方源；

## 1.2.8（2023/6/9）

fix

- 修复了 `pypi` 安装 `numpy` 存在系统安全管控的问题；

## 1.2.7（2023/6/8）

fix

- `env.sh` 中安装 `Python` 包未指定版本时，日志输出安装的版本；

  ```shell
  pdocr-rpc                       2.0.1
  allure-custom                   1.2.1
  funnylog                        1.1.3
  ```

- 修复 `-f` 测试套件执行报错的的问题；

## 1.2.6（2023/6/7）

fix

- 修复 `wayland` 上调用鼠标中键、右键不生效的问题；
- 修复 `pubilic/dde_desktop_public_widget` 里面通过配置文件定位桌面文件的方法，坐标没有拆包的问题；
- 优化了等待的日志输出；
- `pycreeze` 版本升级到 `0.1.29`，导致与 `pyautogui` `0.9.53` 不兼容，`env.sh` 里面增加指定 `pycreeze` 版本为 `0.1.28`；


## 1.2.5（2023/5/16）

new

-  `--app` 参数后面新增支持 `autotest_xxx` 和 `apps/autotest_xxx` 两种写法，目前支持三种参数传入方式：

  ```shell
  ~$: youqu run -a deepin-music
  ~$: youqu run -a autotest_deepin_music
  ~$: youqu run -a apps/autotest_deepin_music
  ```

​		后两种入参方式可以很方便在输入命令的过程中使用补全。

- remote 远程执行新增从命令行传入测试机信息，远程机器的`user@ip:password`,多个机器用'/'连接,如果 `password` 不传入,默认取 `setting/remote.ini` 中 `CLIENT_PASSWORD` 的值,比如：`uos@10.8.13.xx:1` 或 `uos@10.8.13.xx` ；

  ```shell
  python3 manage.py remote -c uos@10.8.13.xx/uos@10.8.13.xx
  python3 manage.py remote -c uos@10.8.13.xx:1/uos@10.8.13.xx:2
  ```

fix

- 日志模块修改为函数执行之前打印日志；
- 日志模块增加白名单，通过类名开头，结束，包含等关键字控制需要打印的函数日志；
- 远程执行时，如果传入了 `app_name` 只会将 `apps` 目录下 `app_name` 的目录发送到测试机；
- `env.sh` 移除 `python3-dev`；
- 修复 `Wayland` 下 `env.sh` 环境安装失败的问题，优化了 `deb` 依赖安装的逻辑；
- 将 `env.sh` 刷新源的日志在终端显示，解决在 `CI` 环境下，长时间不输出日志连接中断的问题；
- 修复`1060` 华为机型安装键鼠工具时依赖不兼容的问题；

## 1.2.4（2023/2/27）

fix

- 修改 `CURRENT` 文件；

## 1.2.3（2023/2/27）

new

- `pylint.sh` 支持通过位置参数传入文件路径：`bash pylint.sh apps/autotest_deepin_music`,好处是参数路径可以在终端补全；
- 新增系统命令 `youqu-pylint` ，用于静态代码扫描，使用方法: `youqu-pylint apps/autotest_deepin_music`；
- 由于系统一些 `dbus` 接口改变，公共库中的 `dbus` 方法将不再维护，由子项目在 `other_widget.py` 里面进行维护；

fix

- 修复 `ssh` 环境下运行提示 “无法连接” 的问题；
- 修复运行时程序退出，不输出异常日志的问题；
- 修复`youqu remote xxx` 远程执行时，在服务端 `Ctrl + C` 无法停止程序运行的问题；

## 1.2.2（2023/2/8）

new

- 新增气泡类图像识别方案；`image_utils.py::ImageUtil::get_during`；
- 图像识别新增指定区域识别，传入 `[x, y, w, h]`，x: 左上角横坐标；y: 左上角纵坐标；w: 宽度；h: 高度；根据匹配度返回坐标；
- 图像识别新增指定目标图片，传入目标图片路径；
- `env.sh` 移除 `pypinyin`;
- 优化执行 `env.sh` 时的日志输出；
- `manage.py` 移除了参数 `session_timeout` ，框架根据全局的 `timeout` 以及用例自定义的 `timeout` 自动计算出 `sessiontimeout` 的值；
- 新增 ocr 服务器链接重试，默认重试1次，支持动态传入参数；

fix

- 修复了一些 pylint 扫描的代码风格问题；
- 重新设计了测试报告主题；

## 1.2.1（2023/1/6）

new

- 支持使用系统命令 `youqu` 执行用例；可将`python3 manage.py` 替换为 `youqu` ：

  ``` shell
  youqu run -a deepin-music -k 001
  ```

- `RPC` 服务 `IP` 地址修改为域名：http://youqu-dev.uniontech.com，指定不同的端口；
- 在线文档地址修改为域名：http://youqu-dev.uniontech.com，原来的地址 10.8.10.215 将不在使用；

fix

- 修复 `--count` 参数可能出现与其他框架的工程依赖存在冲突，报错重复注册的问题；
- 修复 CI 环境下多个工程存在 Python 环境变量指向错误，导包报错的问题；
- 修复单独运行方法时无日志输出的 Bug；


## 1.2.0（2022/12/30）

1.1.4 版本适配持续集成流水线且新增了较多新特性，我们计划使用 1.1.4 版本运行一段时间，1.2.0 版本将修复期间出现的 Bug，然后作为稳定版本发布。

new

- 修改工程名称为 `youqu`；
- 将 sphinx 文档工程迁移到单独的仓库；

fix

- 修复 startapp 创建工程时存在工程名称时无法继续创建；
- 修复了 OCR 服务在并发时可能出现无法返回结果的问题，提升 OCR 服务高并发稳定性；
- 修复 PMS 同步标签到 CSV 文件不支持用例库的问题；

## 1.1.4（2022/12/14）

new

- 新增 `startapp` 子命令创建子项目工程模板: `python3 manage.py startapp autotest_deepin_xxx`

- 新增指定用例重复执行次数；

- 去掉批量执行前收集用例的步骤；

- 增加开始执行时打印一些执行参数，如：

  ```shell
  用例收集数量:	99
  失败重跑次数:	1
  最大失败次数:	49
  用例超时时间:	200.0s (03分20秒)
  会话超时时间:	11880s (3小时18分0秒)
  ```

- 定制修改allure报告logo、title、默认语言；

- `manage.py` 执行开始时打印 logo 和当前版本：

  ```shell
   ██╗   ██╗  ██████╗  ██╗   ██╗  ██████╗  ██╗   ██╗ 
   ╚██╗ ██╔╝ ██╔═══██╗ ██║   ██║ ██╔═══██╗ ██║   ██║ 
    ╚████╔╝  ██║   ██║ ██║   ██║ ██║   ██║ ██║   ██║ 
     ╚██╔╝   ██║   ██║ ██║   ██║ ██║▄▄ ██║ ██║   ██║ 
      ██║    ╚██████╔╝ ╚██████╔╝ ╚██████╔╝ ╚██████╔╝ 
      ╚═╝     ╚═════╝   ╚═════╝   ╚══▀▀═╝   ╚═════╝  
  
  
   ▄█   ▄█   █ █ 
    █ ▄  █ ▄ ▀▀█ 
  ```

- 新增指定用例执行次数；

  - 装饰器方法指定次数；

    ```python
    @pytest.mark.count(2)
    def test_music_679537():
        pass
    ```

  - 命令行参数指定次数；

    ```shell
    python3 manage.py run -a deepin-music -k 001 --count 2
    ```

- ​	image_utils 增加函数 save_temporary_picture，支持指定屏幕区域截图并返回图片存放的本地路径，后续使用 assert_image_exist 进行断言

  - ```Python
    def test_music_679537(self):
        pic_path = DeepinMusicWidget.save_temporary_picture(x, y, width, height)
        ...... # 中间操作
        self.assert_image_exit(pic_path)
    ```

- button_center 新增 btn_size 获取控件左上角坐标及长宽，用于动态的截取元素的图片，可用于定位断言

  - ```python
    def test_music_679537(self):
        pic_path = DeepinMusicWidget.save_temporary_picture(*DeepinMusicWidget().ui.btn_size("所有音乐按钮"))
        ...... # 中间操作
        self.assert_image_exit(pic_path)
    ```

- allure 报告中定位问题除了日志、截图、录屏外，调用的函数增加了 step 步骤展示；

- `env.sh` 新增安装子项目 `Python` 三方依赖，在子项目根目录下写 `requirement.txt` 文件，`env.sh` 会自动加载；

- ocr 识别新增支持传入目标图片路径进行文字识别，减少因全屏识别时，其他文字的干扰

  - ```Python
    # 断言音乐的删除弹窗中，包含了“确认”的文字
    self.assert_ocr_exist("确认", picture_abspath=DeepinMusicWidget.save_temporary_picture(*DeepinMusicWidget().ui.btn_size("删除弹窗")))
    ```

- 断言函数的调用也会自动打印日志;

- `env.sh` 新增裁剪依赖的方案；

fix

- 修复 `Jenkins` 环境下， `apps` 目录下子项目存在 `auotest_deepin_xxx@tmp` 目录，在传入 `app_name` 后无法执行用例的问题；
- 修复自动生成 `case_list.csv` 文件时，用例顺序被调整的问题；
- `env.sh` 环境安装移除 git 和 curl；
- 修复用例在 setup 阶段报错后，未写入 ci_result.json 的问题；
- 移除 `uos_ci.py`；

## 1.1.3（2022/10/28）

new

- 新增图像断言成功输出匹配度；
- 新增环境安装 yaml 依赖；
- 新增测试套执行、数据回填兼容用例库ID和产品库ID；
- 新增测试结果表情显示，并优化了日志的排版；
- 新增 `--top {number}` 用于记录系统资源占用情况，日志生成到 `report/logs/top.log`；

fix

- 修复用例收集阶段报错，但终端没有错误日志输出的问题；
- 修改失败用例回溯日志为详细级别；
- 修复了执行进度未计算跳过用例的问题，并优化了进度获取的算法；
- 修复 `env.sh` 在 V23 环境下安装无法读取密码的问题；
- 修复了 pms 测试套执行或测试单执行时，用例ID兼容用例库ID和产品库ID；
- env.sh 里面 hub.deepin.com 更换成 it.uniontech.com；
- uos_ci.py 测试结果统计时，总数剔除 skip 的数量

## 1.1.2（2022/09/21）

new

- 在没有安装 `dogtail` 的情况下，也能使用 `sniff` 工具；

fix

- 修复持续集成流水线中没有安装 AT 环境执行 `uos_ci.py` 报错的问题；

## 1.1.1（2022/09/19）

new

- 新增执行进度显示，每条用例执行时日志输出当前进度：[当前指定第几条/用例总数]；
- 新增终端输出用例执行结束之后所有失败用例的列表；
- 关闭终端输出捕获用例执行过程日志快照；
- 优化终端输出失败信息冗长为简要信息输出；
- 新增终端输出显示 10 个执行最慢的用例列表，并详细列出各个阶段的耗时；
- 失败重跑用例重跑之前延迟 1 秒；
- 新增收集阶段报错，仍然强制执行；
- 用例收集时仅在 `apps` 目录下进行，忽略 `src,setting,public` 目录；
- 新增 `allure` 报告备份功能，默认备份至 `allure_back` 目录下；
- `manage.py`新增参数 `--lastfailed` 用于只跑上次失败用例的功能；

fix

- 修复了在没有指定应用名称执行时，xml 报告生成路径异常的问题；
- 修复了 `uos_ci.py` 传入 `timeout` 和 `session_timeout` 不生效的问题；

## 1.1.0（2022/09/16）

new

- 新增PMS数据回填功能，支持多种数据回填模式；
- 优化了通过测试套件执行时PMS 爬虫的性能；
- 新增 `.gitmodules` 文件，用于标记所有子项目，方便统一拉取代码；
- `env.sh` 适配社区版上安装自动化环境；
- 增加执行过程中立即显示错误的功能；
- `README.md` 增加 `Wayland` 下使用、测试报告查看、常见问题等的文档说明；
- 增加了用例执行过程中对 `setup`、`call`、`teardown` 进行日志分段；

fix

- 修复了 `确认修复` 列没写表头，但写了 `fixed-xxx` 标签，出现的程序报错问题；
- 修复了同一应用内多个 `csv` 文件中 `确认修复` 列有的写了，有的没写，可能出现的程序报错的问题；
- 修复了 `INFO` 日志，显示为 `DEBUG` 的问题；修复了部分机器上 `INFO` 日志内容显示为红色的问题；
- 修复了用例收集阶段报错看不到详细信息的问题；

## 1.0.2（2022/08/22）

new

- 移除 `loguru`，替换为 `logging`，接口保持不变，上层用例不受影响；
- 默认开启 `coredump`；

fix

- 修复了三方库 `loguru` 偶现异常，导致程序中断的问题；
- 修复了第一次失败不会关闭文件选择框的问题；

## 1.0.1（2022/08/12）

new

- 新增 `RELEASE.md` 文件，用于记录历史发布版本的更新内容；

- 兼容 `Wayland` 模式下执行用例，上层用例不用管当前测试机执行环境，框架会自动根据当前环境走不同的代码逻辑；
- 由于需要修改 `dogtail` 源代码，因此将修改后的源码放入到核心库里面 `src/depends/dogtail` 后续版本**将**不需要在系统中安装`dogtail`；
- 如果应用库同样使用了系统安装的 `dogtail` 可能会报错，解决方案是将代码中的 `import dogtail` 修改为 `from src.depends import dogtail` ;

fix

- 重跑失败之后才会关闭文件选择框，修改为失败之后会关闭文件选择框；





