# AT 执行器使用指北

```plain
# =============================================
# Attribution : Chengdu Test Department
# Time        : 2022/5/25
# Author      : litao
# =============================================
```
Jenkins url: [https://jenkinswh.uniontech.com/view/CI/job/chengdu/job/AT_test/](https://jenkinswh.uniontech.com/view/CI/job/chengdu/job/AT_test/)
## 1、功能介绍

* 支持任意测试机系统语言设置，分辨率设置及用例执行环境搭建；
* 支持 IP 为 15 网段的 AMD 架构测试机镜像装机；
* 支持任意测试机指定应用，指定范围标签的用例执行；
* 支持任意测试机状态检查，是否有正在运行的测试；
* 支持配置用例执行时长，防止任务阻塞；
* 支持根据应用版本自动查找对应的用例 tag；
* 支持异常处理和测试完成的实时消息通知；
## 2、Job 介绍

以下按执行流程的顺序介绍，每一步都可以单独执行。

### 1、主入口

Jenkins url: [https://jenkinswh.uniontech.com/view/CI/job/chengdu/job/AT_test/job/AT_test/](https://jenkinswh.uniontech.com/view/CI/job/chengdu/job/AT_test/job/AT_test/)

整个流程的主入口，通过这个入口，连同整个测试流程，镜像装机，环境部署，测试应用及生成报告。

参数介绍：

* 测试机：所有规整到固定区域的测试机，通过测试同学对测试机的习惯命名，在后台映射测试机的详细信息，括号中为测试机 IP 的最后一位；
* 测试应用：指定的测试应用的包名，系统根据名称自动拉取对应的仓库代码；
* deb包下载地址：测试上述应用时，需要安装的deb包下载地址，多个地址用“,”隔开，可以为空；
* 范围标签：执行测试用例的标签范围，对应用例代码 csv 文件中的标签信息，以 pytest 的mark语法编写；
* 系统语言：设置测试机执行用例时的系统语言环境；
* 分辨率：设置测试机执行用例时的系统分辨率环境；
* 镜像地址：镜像仓库的下载地址，通过 PXE 装机，可以为空，则直接跳过装机环节（目前仅支持部分 AMD 架构的装机）；
### 2、PXE 装机

Jenkins url: [https://jenkinswh.uniontech.com/view/CI/job/chengdu/job/AT_test/job/IOS_install/](https://jenkinswh.uniontech.com/view/CI/job/chengdu/job/AT_test/job/IOS_install/)

输入测试机的用户名，IP，密码，镜像地址后，自动装机，目前仅支持固定 15 网段的部分 AMD 架构的测试机。

### 3、次主入口

Jenkins url: [https://jenkinswh.uniontech.com/view/CI/job/chengdu/job/AT_test/job/all_client_test/](https://jenkinswh.uniontech.com/view/CI/job/chengdu/job/AT_test/job/all_client_test/)

该入口与主入口功能基本一致，只是剥离了PXE装机流程，支持任意测试机的执行流程。

### 4、环境部署

Jenkins url：[https://jenkinswh.uniontech.com/view/CI/job/chengdu/job/AT_test/job/env/build?delay=0sec](https://jenkinswh.uniontech.com/view/CI/job/chengdu/job/AT_test/job/env/build?delay=0sec)

设置测试机的系统语言，分辨率及安装测试所需的依赖包。

### 5、发送代码

Jenkins url: [https://jenkinswh.uniontech.com/view/CI/job/chengdu/job/AT_test/job/send_code/](https://jenkinswh.uniontech.com/view/CI/job/chengdu/job/AT_test/job/send_code/)

根据测试应用名称，拉取对应的应用库代码，并根据测试机上应用版本切换到对应的tag版本，若未找到tag版本，则使用最新的应用库代码，再根据应用库代码中配置的基础库版本，拉取基础库代码。

### 6、用例执行

Jenkins url: [https://jenkinswh.uniontech.com/view/CI/job/chengdu/job/AT_test/job/run_test/](https://jenkinswh.uniontech.com/view/CI/job/chengdu/job/AT_test/job/run_test/)

运行测试机上的用例



