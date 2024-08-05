# DBus交互

导入：

```python
from youqu3.dbus import DBus
```

使用：

```python
info = {
        "service_name": "org.kde.KWin",
        "path": "/Screenshot",
        "interface": "org.kde.kwin.Screenshot",
    }
res = DBus(**info).session.method("screenshotFullscreen").send()
print(res)
```

底层调用 `dbus-send` 做 DBus 操控。
