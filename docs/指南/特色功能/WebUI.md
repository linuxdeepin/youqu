# WebUI

YouQu 基于 `Playwright` 驱动浏览器实现 WebUI 自动化测试。

市面上耳熟能详的可用于 `Web UI` 自动化测试工具：`Selenium`、`Cypress`、`Puppeteer`、`Playwright`；

咱们先初步排除掉一些明显不用的：

- `Cypress`，只支持 `JavaScript`，而我们自动化人员大多使用 `Python` 对 `JavaScript` 不熟悉，排除。
- `Puppeteer`，只支持谷歌浏览器，格局没打开，官方不支持 `Python`，排除。

剩下 `Selenium`、`Playwright`，我们从一些方面做对比：

| 对比指标     | Selenium | Playwright |
| :----------- | :------: | :--------: |
| 环境安装难度 |    ✗     |     ✔      |
| 运行速度     |    ✗     |     ✔      |
| 元素等待     |    ✗     |     ✔      |
| 智能定位     |    ✗     |     ✔      |
| 稳定性       |    ✔     |     ✔      |
| 文档         |    ✔     |     ✗      |
| 接口测试     |    ✗     |     ✔      |

总结：

`Playwright` 作为一个比较新的工具，在文档方便确实没有老牌的 `Selenium` 完善，特别是一些示例、方法的使用说明，都还不够好，甚至有些就没有说明，但基本的使用该有的都有。

除了文档方面，`Playwright` 几乎在各方面碾压 `Selenium`，很明显 `Playwright` 以绝对优势获胜。

## 实践方法

参考章节 [【Web UI 自动化测试】](https://youqu.uniontech.com/%E5%AE%9E%E8%B7%B5/WebUI%E8%87%AA%E5%8A%A8%E5%8C%96%E6%B5%8B%E8%AF%95/%E5%88%9D%E5%A7%8B%E5%8C%96%E9%A1%B9%E7%9B%AE.html)

## 断言方法

`YouQu` 框架统一提供断言语句，以保持统一的断言语句风格。

```python
# src/webui.py

class WebAssert:
    
    @staticmethod
    def assert_locator(
        locator: Union[Page, Locator, APIResponse],
    ) -> Union[PageAssertions, LocatorAssertions, APIResponseAssertions]:
        return _expect(locator)
```

