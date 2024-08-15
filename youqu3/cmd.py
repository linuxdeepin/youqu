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


class RemoteCmd:

    def __init__(self, user: str, ip: str, password: str):
        self.user = user
        self.ip = ip
        self.password = password

    def remote_run(self, cmd: str, return_code: bool = False, timeout: int = None):
        res = Cmd.expect_run(
            f'ssh {self.user}@{self.ip} "{cmd}"',
            events={'password': f'{self.password}\n'},
            return_code=return_code,
            timeout=timeout
        )
        if return_code is False:
            return res.decode("utf-8")
        stdout, return_code = res
        return stdout.decode("utf-8"), return_code

    def remote_sudo_run(self, cmd: str, workdir: str = None, return_code: bool = False):
        wd = ""
        if workdir is not None:
            _, code = self.remote_run(f"ls {workdir}", return_code=True)
            if code == 0:
                wd = workdir
            else:
                raise FileNotFoundError(workdir)
        return self.remote_run(f"{wd}echo '{self.password}' | sudo -S {cmd}", return_code=return_code)
