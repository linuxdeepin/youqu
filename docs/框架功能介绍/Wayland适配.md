## Wayland 适配

`Wayland` 下自动化主要问题是 `X11` 下的键鼠操作方法无法使用，比如 `Xdotool`、 `PyAutoGUI`、`Xwininfo` 等等；

YouQu 在 `Wayland` 下兼容适配，`env.sh` 在 `Wayland` 下执行时会安装自研的键鼠操作服务（可能存在一些依赖报错，按照注释解决即可），框架核心库也针对性的做了适配，上层用例完全不用关心机器是`Wayland`  还是 `X11`，框架会根据执行时状态自动判断走不同的逻辑；

简单讲就是，应用库只需要维护一套用例脚本即可。

【用例兼容】

因为 `Wayland` 下有些应用的界面显示和功能本身存在一些差异，用例层可能需要对这部分用例做逻辑判断，使用全局配置里面的常量进行逻辑编写即可：

```python
from setting.globalconfig import GlobalConfig

# GlobalConfig.IS_WAYLAND 获取到当前的显示服务器（bool）
# 应用库 Config 继承 GlobalConfig
if Config.IS_WAYLAND:
    pass
if Config.IS_X11:
    pass
```

比如用例里面如果断言的图片不同：

```python
if Config.IS_WAYLAND:
    self.assert_image_exist("wayland_XXX")
else:
    self.assert_image_exist("x11_XXX")
```

这样这条用例脚本在 `Wayland` 和 `X11` 下都可以跑，so easy 是不是？完全没必要专门拉新分支进行 `Wayland` 适配。
