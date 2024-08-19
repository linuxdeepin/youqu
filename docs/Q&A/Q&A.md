# Q&A

::: details 安装提示网络超时或安装缓慢
添加镜像源：`-i https://pypi.tuna.tsinghua.edu.cn/simple`

或直接添加镜像源到 pip 全局配置里面：
```bash
pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```
:::

::: details youqu3:未找到命令
添加环境变量：
```bash
export PATH=$PATH:$HOME/.local/bin
```

建议将其添加到 ~/.bashrc 里面。
:::

::: details 开发环境：Pycharm 添加 pipenv 虚拟环境时提示找不到 pipenv
Pycharm 没有在环境变量中找到 pipenv，可以尝试：
```bash
sudo pip3 install pipenv
```
:::