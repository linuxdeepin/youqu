# 版本更新记录

## 1.3.1（unreleased）

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

- remote 远程执行新增从命令行传入测试机信息，远程机器的`user@ip:password`,多个机器用'/'连接,如果 `password` 不传入,默认取 `setting/remote.ini` 中 `CLIENT_PASSWORD` 的值,比如：`uos@10.8.13.33:1` 或 `uos@10.8.13.33` ；

  ```shell
  python3 manage.py remote -c uos@10.8.13.33/uos@10.8.13.34
  python3 manage.py remote -c uos@10.8.13.33:1/uos@10.8.13.34:2
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
    def test_music_001():
        pass
    ```

  - 命令行参数指定次数；

    ```shell
    python3 manage.py run -a deepin-music -k 001 --count 2
    ```

- ​	image_utils 增加函数 save_temporary_picture，支持指定屏幕区域截图并返回图片存放的本地路径，后续使用 assert_image_exist 进行断言

  - ```Python
    def test_music_001(self):
        pic_path = DeepinMusicWidget.save_temporary_picture(x, y, width, height)
        ...... # 中间操作
        self.assert_image_exit(pic_path)
    ```

- button_center 新增 btn_size 获取控件左上角坐标及长宽，用于动态的截取元素的图片，可用于定位断言

  - ```python
    def test_music_001(self):
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





