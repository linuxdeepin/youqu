# Ruff格式化工具

YouQu 默认使用 Python 最强代码检查&格式化工具——Ruff。

## 安装

```shell
pip install ruff
```

## 代码检查

代码检查是扫描代码中存在的问题。

```shell
ruff check .
```

表示扫描当前目录下所有的代码，当然你可以指定一个具体的目录或文件。

![](/指南/框架必备/ruff-2.png)

在扫描日志最后可以看到一个 `fixable`，意思是可以通过 `--fix` 参数直接给你修复掉。

```shell
ruff check setting/ --fix
```

对比下文件前后：

![](/指南/框架必备/ruff-3.png)

你看，直接修复了对吧。

## 代码格式化

经过前面代码检查并修复之后，说明我们代码中没有“问题”了，接下来就可以进行代码格式化。

```shell
ruff format setting/
```

![](/指南/框架必备/ruff-4.png)

效果很不错对吧。

格式化这块 Ruff 官方表示是可以直接替代 Black 的。

## 配置

前面代码检查的时候报了一个问题，是说在 `__init__.py` 文件里面写了一个导入，但没有被使用。

但是这是我特意这样写的，是一种名称空间的设计，可以在 `setting` 名称空间下直接导入，不需要 Ruff 处理这个问题，这也不是个问题。

因此，我们需要对 Ruff 进行配置。

在根目录下 `ruff.toml` 的文件：

```toml
# Exclude a variety of commonly ignored directories.
exclude = [
    ".bzr",
    ".direnv",
    ".eggs",
    ".git",
    ".git-rewrite",
    ".hg",
    ".ipynb_checkpoints",
    ".mypy_cache",
    ".nox",
    ".pants.d",
    ".pyenv",
    ".pytest_cache",
    ".pytype",
    ".ruff_cache",
    ".svn",
    ".tox",
    ".venv",
    ".vscode",
    "__pypackages__",
    "_build",
    "buck-out",
    "build",
    "dist",
    "node_modules",
    "site-packages",
    "venv",
]

# Same as Black.
line-length = 100
indent-width = 4

# Assume Python 3.7
target-version = "py37"

[lint]
# Enable Pyflakes (`F`) and a subset of the pycodestyle (`E`)  codes by default.
# Unlike Flake8, Ruff doesn't enable pycodestyle warnings (`W`) or
# McCabe complexity (`C901`) by default.
select = ["E4", "E7", "E9", "F"]
ignore = []

# Allow fix for all enabled rules (when `--fix`) is provided.
fixable = ["ALL"]
unfixable = []

# Allow unused variables when underscore-prefixed.
dummy-variable-rgx = "^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"

[format]
# Like Black, use double quotes for strings.
quote-style = "double"

# Like Black, indent with spaces, rather than tabs.
indent-style = "space"

# Like Black, respect magic trailing commas.
skip-magic-trailing-comma = false

# Like Black, automatically detect the appropriate line ending.
line-ending = "auto"

# Enable auto-formatting of code examples in docstrings. Markdown,
# reStructuredText code/literal blocks and doctests are all supported.
#
# This is currently disabled by default, but it is planned for this
# to be opt-out in the future.
docstring-code-format = false

# Set the line length limit used when formatting code snippets in
# docstrings.
#
# This only has an effect when the `docstring-code-format` setting is
# enabled.
docstring-code-line-length = "dynamic"
```

在上面配置文件中 `ignore = []` 写入错误代码：

```toml
ignore = ["F401"]
```

再次扫描就不会再报之前的问题。

其他的一些配置也可以根据自己的一些需要进行配置。
