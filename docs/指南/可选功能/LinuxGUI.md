# Linux GUI

[PyLinuxAuto](https://youqu.uniontech.com/pylinuxauto/) 是专注于 Linux GUI 自动化测试的框架，提供丰富的键鼠控制及多种元素定位方案。

## 安装

```bash  
pip install "youqu3[gui]"
```

## 使用说明

### 导入

```python
from youqu3.gui import pylinuxauto
```

### 键鼠控制

```python
pylinuxauto.click()
pylinuxauto.double_click()
```

[了解更多...](https://youqu.uniontech.com/pylinuxauto/%E6%8C%87%E5%8D%97/%E9%94%AE%E9%BC%A0%E6%93%8D%E4%BD%9C.html)

### 属性定位

```python
pylinuxauto.find_element_by_attr_path("/dde-dock/Btn_文件管理器").click()
```

[了解更多...](https://youqu.uniontech.com/pylinuxauto/%E6%8C%87%E5%8D%97/%E5%B1%9E%E6%80%A7%E5%AE%9A%E4%BD%8D.html)

### 图像识别

```python
pylinuxauto.find_element_by_image("~/Desktop/test.png").click()
```

[了解更多...](https://youqu.uniontech.com/pylinuxauto/%E6%8C%87%E5%8D%97/%E5%9B%BE%E5%83%8F%E8%AF%86%E5%88%AB.html)

### OCR识别

```python
pylinuxauto.find_element_by_ocr("中国").click()
```

[了解更多...](https://youqu.uniontech.com/pylinuxauto/%E6%8C%87%E5%8D%97/OCR%E8%AF%86%E5%88%AB.html)

### 相对位移定位

```python
pylinuxauto.find_element_by_ui(
    appname="dde-file-manager",
    config_path="~/Desktop/ui.ini",
    btn_name="最大化按钮"
).click()
```

[了解更多...](https://youqu.uniontech.com/pylinuxauto/%E6%8C%87%E5%8D%97/%E7%9B%B8%E5%AF%B9%E4%BD%8D%E7%A7%BB%E5%AE%9A%E4%BD%8D.html)