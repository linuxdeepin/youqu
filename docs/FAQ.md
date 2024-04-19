---
hide:
    - navigation
---

## 1. 提交代码时提示邮箱或者名称不对

重新配置邮箱或者名称，然后重置生效：

```shell
git commit --amend --reset-author
```

---------------

## 2. 怎么回滚到之前的版本

(1)查询历史提交记录

```shell
git log
```

找到你要回滚的版本，复制 `hash` 值。

- 注意：是 `commit` 空格之后的 `hash` 值，之前有同学复制的 `Change-Id:` 这样肯定报错。

(2)回滚版本，不清除代码

```shell
git reset --soft ${hash}
```

(3)回滚版本，清除代码，慎用哈

```shell
git reset --hard ${hash}
```

---------------------------

## 3. 解决 git status 中文显示的问题

```shell
git config --global core.quotePath false
```

---------------------

## 4. `apps` 目录下颜色有些是黄色的

在 `Pycharm` 中 `apps` 目录下应用库文件是黄色的，编辑器识别不到代码新增和修改；

由于社区版 `Pycharm` 不能动态识别多仓库，需要在 setting 里面手动注册，操作步骤：

`File` —`Settings` —`Version Control` —点 `+` 号  —`Directory` 选中应用库工程目录  —`VCS` 选中 `Git` —`Apply`

如此就可以了。

专业版 `Pycharm` 一般不存在这个问题。

------------------------------

## 5. 执行 `env.sh` 报错 `$'\r':未找到命令`

出现这个问题你应该是在 windows 上打开或编辑过 `env.sh` 脚本，windows下的换行是回车符+换行符，也就是`\r\n`，而 `Linxu` 下是换行符 `\n`，`Linux` 下不识别 `\r`，因此报错。

解决方案：

```shell
# 将 \r 替换为空
sudo sed -i 's/\r//' env.sh
```

---------------------------

## 6. 怎样为单独某一条用例配置执行超时时间

在用例脚本中添加装饰器，如下：

```python
@pytest.mark.timeout(300) # 单位秒
def test_xxx_001():
	pass
```

-----------------------

## 7. 如何修复子仓库 master 分支游离头（detached head）

修复所有子仓库默认master 分支游离头

```shell
cd  youqu
git submodule foreach -q --recursive 'git checkout $(git config -f $toplevel/.gitmodules submodule.$name.branch || echo master)'
```

-------------------------
