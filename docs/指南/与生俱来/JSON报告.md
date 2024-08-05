# JSON 报告

框架默认生成 JSON 报告，在用例工程目录下生成报告文件： `/report/json/report_xxxx.json`

## 报告内容

### 整体结构

```json
{
    "created": 1518371686.7981803,
    "duration": 0.1235666275024414,
    "exitcode": 1,
    "root": "/path/to/tests",
    "environment": ENVIRONMENT,
    "summary": SUMMARY,
    "collectors": COLLECTORS,
    "tests": TESTS,
    "warnings": WARNINGS,
}
```

### Environment

环境信息

```json
{
    "Python": "3.6.4",
    "Platform": "Linux-4.56.78-9-ARCH-x86_64-with-arch",
    "Packages": {
        "pytest": "3.4.0",
        "py": "1.5.2",
        "pluggy": "0.6.0"
    },
    "Plugins": {
        "xdist": "1.22.0",
        "metadata": "1.5.1",
    },
    "foo": "bar"
}
```

### Summary

汇总信息

```json
{
    "collected": 10,
    "passed": 2,
    "failed": 3,
    "xfailed": 1,
    "xpassed": 1,
    "error": 2,
    "skipped": 1,
    "total": 10
}
```

### Collectors

收集器节点的列表，默认关闭，不显示。

### Tests

每个用例的详细结果

```json
[
    {
        "nodeid": "test_foo.py::test_fail",
        "lineno": 50,
        "keywords": [
            "test_fail",
            "test_foo.py",
            "test_foo0"
        ],
        "outcome": "failed",
        "setup": TEST_STAGE,
        "call": TEST_STAGE,
        "teardown": TEST_STAGE,
        "metadata": {
            "foo": "bar",
        }
    },
    ...
]
```

### Warnings

警告信息

```json
[
    {
        "code": "C1",
        "path": "/path/to/tests/test_foo.py",
        "nodeid": "test_foo.py::TestFoo",
        "message": "cannot collect test class 'TestFoo' because it has a __init__ constructor"
    }
]
```

