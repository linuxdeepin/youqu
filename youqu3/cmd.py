import os
import subprocess
import sys

from youqu3 import exceptions
from youqu3 import logger
from youqu3 import setting


class Cmd:

    @staticmethod
    def _run(command, _input=None, timeout=None, check=False, executable=None, **kwargs):
        with subprocess.Popen(command, **kwargs) as process:
            try:
                stdout, stderr = process.communicate(_input, timeout=timeout)
            except:
                process.kill()
                raise
            retcode = process.poll()
            if check and retcode:
                raise subprocess.CalledProcessError(
                    retcode, process.args, output=stdout, stderr=stderr
                )
        return subprocess.CompletedProcess(process.args, retcode, stdout, stderr)

    @classmethod
    def _getstatusoutput(cls, command, timeout, executable):
        kwargs = {
            "shell": True,
            "stderr": subprocess.STDOUT,
            "stdout": subprocess.PIPE,
            "timeout": timeout,
            "executable": executable,
        }
        try:
            if sys.version_info >= (3, 7):
                kwargs["text"] = True
            result = cls._run(command, **kwargs)
            data = result.stdout
            if isinstance(data, bytes):
                data = data.decode("utf-8")
            exitcode = result.returncode
        except subprocess.CalledProcessError as ex:
            data = ex.output
            exitcode = ex.returncode
        except subprocess.TimeoutExpired as ex:
            data = ex.__str__()
            exitcode = -1
        if data[-1:] == "\n":
            data = data[:-1]
        return exitcode, data

    @classmethod
    def run(
            cls,
            command: str,
            interrupt: bool = False,
            timeout: [None, int] = 25,
            print_log: bool = True,
            command_log: bool = True,
            return_code: bool = False,
            executable: str = "/bin/bash",
    ):
        """
         执行shell命令
        :param command: shell 命令
        :param interrupt: 命令异常时是否中断
        :param timeout: 命令执行超时
        :param out_debug_flag: 命令返回信息输出日志
        :param command_log: 执行的命令字符串日志
        :return: 返回终端输出
        """
        exitcode, stdout = cls._getstatusoutput(command, timeout=timeout, executable=executable)
        if command_log:
            logger.debug(command)
        if exitcode != 0 and interrupt:
            raise exceptions.ShellExecutionFailed(stdout)
        if print_log and stdout:
            logger.debug(stdout)
        if return_code:
            return stdout, exitcode
        return stdout

    @staticmethod
    def expect_run(
            cmd: str,
            events: dict,
            return_code=False,
            timeout: int = 30
    ):
        """
        expect_run(
            "ssh username@machine_ip 'ls -l'",
            events={'password':'secret\n'}
        )
        如果 return_code=True，返回 (stdout, return_code)
        """
        import pexpect
        return pexpect.run(
            cmd,
            events=events,
            withexitstatus=return_code,
            timeout=timeout
        )

    @classmethod
    def sudo_run(
            cls,
            command,
            password: str = None,
            workdir: str = None,
            interrupt: bool = False,
            timeout: int = 25,
            print_log: bool = True,
            command_log: bool = True,
            return_code: bool = False
    ):
        if password is None:
            password = setting.PASSWORD
        wd = ""
        if workdir:
            if not os.path.exists(workdir):
                raise FileNotFoundError
            wd = f"cd {workdir} && "
        res = cls.run(
            f"{wd}echo '{password}' | sudo -S {command}",
            interrupt=interrupt,
            timeout=timeout,
            print_log=print_log,
            command_log=command_log,
            return_code=return_code
        )
        if return_code is False:
            return res.lstrip("请输入密码●")
        else:
            res = list(res)
            res[0] = res[0].lstrip("请输入密码●")
            return res

    GREP_LIST = (
        "grep",
        "pytest",
        "python",
        "ffmpeg",
        "youqu",
    )

    @classmethod
    def get_process_status(cls, app: str, grep_list: str = None) -> bool:
        """
         获取进程状态
        :param app: 应用包名
        :return: Boolean
        """
        if grep_list:
            cls.GREP_LIST = grep_list
        cmd = ""
        for i in cls.GREP_LIST:
            cmd += f"grep -v {i} | "
        cmd_txt = f"ps -aux | grep {app} | {cmd.rstrip('| ')}"
        logger.debug(cmd_txt)
        result = cls.run(cmd_txt)
        if result:
            logger.debug(result)
            return True
        return False

    @classmethod
    def kill_process(cls, process, grep_list: [list, tuple] = None):
        """
         杀进程
        :param process: 进程名
        """
        if grep_list:
            cls.GREP_LIST = grep_list
        cmd = ""
        for i in cls.GREP_LIST:
            cmd += f"grep -v {i} | "
        cls.run(f"ps -ef | grep {process} | {cmd}cut -c 9-15 | xargs kill -9 > /dev/null 2>&1")

    @classmethod
    def sudo_kill_process(cls, process, grep_list: [list, tuple] = None):
        if grep_list:
            cls.GREP_LIST = grep_list
        cmd = ""
        for i in cls.GREP_LIST:
            cmd += f"grep -v {i} | "
        from youqu3 import setting
        cls.run(
            f"process=$(ps -ef | grep {process} | {cmd}cut -c 9-15);echo '{setting.PASSWORD}' | sudo -S kill -9 $process > /dev/null 2>&1"
        )



class RemoteCmd:

    def __init__(self, user: str, ip: str, password: str, connect_timeout: int = None):
        self.user = user
        self.ip = ip
        self.password = password
        self.connect_timeout = connect_timeout

    def remote_run(self, cmd: str, return_code: bool = False):
        try:
            from fabric import Connection
        except ImportError:
            raise exceptions.YouQuPluginDependencyError("fabric")
        c = Connection(
            host=self.ip,
            user=self.user,
            connect_timeout=self.connect_timeout,
            connect_kwargs={'password': self.password},
        )
        res = c.run(cmd)
        if return_code:
            return res.stdout, res.return_code
        return res.stdout

    def remote_sudo_run(self, cmd: str, return_code: bool = False):
        try:
            from fabric import Connection, Config
        except ImportError:
            raise exceptions.YouQuPluginDependencyError("fabric")
        c = Connection(
            host=self.ip,
            user=self.user,
            config=Config(overrides={'sudo': {'password': self.password}}),
            connect_timeout=self.connect_timeout,
            connect_kwargs={'password': self.password},
        )
        res = c.sudo(cmd)
        if return_code:
            return res.stdout, res.return_code
        return res.stdout

    def remote_expect_run(self):
        # TODO
        ...
