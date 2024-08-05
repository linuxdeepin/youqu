# WebUI

## 安装

```bash
pip install "youqu3[webui]"
```

## 方法编写

方法基类 `base_method.py:: BaseMethod` ：

```python
from youqu3.webui import WebUI

class BaseMethod(WebUI):

    def __init__(self, page):
        super().__init__(page)
```

方法主文件里面：`baidu.py::BaiDu`：

```python
from method.base_method import BaseMethod

class BaiDu(BaseMethod):

    def goto_baidu(self):
        """访问百度首页"""
        self.goto("http://www.baidu.com")

    def click_search_box(self):
        """点击搜索框"""
        self.method.locator("#kw").click()

    def input_keywords(self, keywords):
        """搜索框中输入关键词"""
        self.method.locator("#kw").fill(keywords)
```

## 用例编写

所有的用例都在 `case` 目录下，用例文件以 `test_` 开头，用例 ID 结尾：`test_mycase_001.py`

::: tip test_mycase_001.py

```python
from case import BaseCase
from method.baidu import BaiDu

class TestMyCase(BaseCase):

    def test_mycase_001(self, page):
        """百度首页搜索 YouQu """

        browser = BaiDu(page)
        # 在浏览器访问百度首页
        browser.goto_baidu()
        # 点击搜索框
        browser.click_search_box()
        # 输入YouQu
        browser.input_keywords("YouQu")
        self.assert_locator()
```

:::

- YouQu 提供一个全局默认的对象：`page`，默认使用系统自带的浏览器进行测试；如果需要指定其他第三方的浏览器，提供配置项可以指定浏览器对应的路径。
- 还需要提供一个对象：`native_page`，它使用 `Playwright` 最新的 `Chromium` 浏览器进行测试。