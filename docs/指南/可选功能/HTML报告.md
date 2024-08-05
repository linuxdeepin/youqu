# HTML报告

YouQu3 默认生成测试报告 `元数据`，支持通过`报告生成器`生成 HTML 报告。

### 服务器生成模式  <Badge type="warning" text="默认" />

YouQu3 在所有用例执行完之后，默认使用远程测试报告生成服务器生成 HTML 报告，并暴露 HTTP 服务，且 HTTP 服务的 URL 会返回给测试机生成到 report 目录下，用户可以随时访问。

这样做的好处：

1、省去了测试机上 HTML 测试报告的依赖。

2、测试报告可以做持久化留存，随时可以访问，不用担心测试机上被删掉或重装，任何的流水线都不需要再单独处理测试报告数据持久化的问题。

3、YouQu3 可以做简易版的调用次数统计，之前我一直在想，如何能方便的统计 YouQu 框架到底被使用了多少次，或许测试报告服务器模式是一种比较简单粗暴但很直接的统计方法。

#### 插件安装

基础环境并不包含报告生成器，需要指定安装报告插件或测试类型，如：

```bash
pip install youqu-html-rpc
```

或

```bash
pip install "youqu3[gui]"
```

### 本地生成模式 <Badge type="warning" text="youqu-html 插件" />

如果已安装插件 `youqu-html` ，YouQu3 默认在本地生成 HTML 测试报告，您可以在 report 查看。

#### 插件安装

```bash
pip install youqu-html
```