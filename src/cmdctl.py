#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

import os
# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
import subprocess
import sys

from setting import conf
from src import logger
from src.custom_exception import ShellExecutionFailed


class CmdCtl:
    """命令行工具"""

    # pylint: disable=too-many-arguments,too-many-locals,too-many-public-methods
    # clean_env也要用
    GREP_LIST = (
        "grep",
        "pytest",
        "python",
        "asan",
        "tee",
        "ffmpeg",
        "youqu",
    )

    @staticmethod
    def _run(command, _input=None, timeout=None, check=False, **kwargs):
        """run"""
        with subprocess.Popen(command, **kwargs) as process:
            try:
                stdout, stderr = process.communicate(_input, timeout=timeout)
            except:  # Including KeyboardInterrupt, communicate handled that.
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
        """getstatusoutput"""
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
            result = cls._run(command, **kwargs
                              )
            data = result.stdout
            if isinstance(data, bytes):
                data = data.decode("utf-8")
            exitcode = result.returncode
        except subprocess.CalledProcessError as ex:
            data = ex.output
            exitcode = ex.returncode
        except subprocess.TimeoutExpired as ex:
            # pylint: disable=unnecessary-dunder-call
            data = ex.__str__()
            exitcode = -1
        if data[-1:] == "\n":
            data = data[:-1]
        return exitcode, data

    @classmethod
    def sudo_run_cmd(
            cls,
            command,
            workdir: str = None,
            interrupt: bool = False,
            timeout: int = 25,
            out_debug_flag: bool = True,
            command_log: bool = True,
            password: str = None,
    ):
        if password is None:
            password = conf.PASSWORD
        wd = ""
        if workdir:
            if not os.path.exists(workdir):
                raise FileNotFoundError
            wd = f"cd {workdir} && "
        return cls.run_cmd(
            f"{wd}echo '{password}' | sudo -S {command}",
            interrupt=interrupt,
            timeout=timeout,
            out_debug_flag=out_debug_flag,
            command_log=command_log,
        )

    @classmethod
    def run_cmd(
            cls,
            command,
            interrupt=False,
            timeout=25,
            out_debug_flag=True,
            command_log=True,
            executable="/bin/bash"
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
        status, out = cls._getstatusoutput(command, timeout=timeout, executable=executable)
        if command_log:
            logger.debug(command)
        if status and interrupt:
            raise ShellExecutionFailed(out)
        if out_debug_flag and out:
            logger.debug(out)
        return out

    @classmethod
    def monitor_process(cls, app_name, grep_list: str = None):
        """
         监控进程状态
        :param app_name: 应用包名
        :return: 进程 ID，进程名，
        """
        if grep_list:
            cls.GREP_LIST = grep_list
        cmd = ""
        for i in cls.GREP_LIST:
            cmd += f"grep -v {i} | "
        ps_grep_v_str = (
            f"ps -aux | grep {app_name} | {cmd.rstrip('| ')} | "
            # pylint: disable=anomalous-backslash-in-string
            "grep -v daemon | grep -v '\-d'"
        )

        p_id = cls.run_cmd(
            # pylint: disable=consider-using-f-string
            "%s | awk '{print $2}'" % ps_grep_v_str,
            interrupt=False,
            command_log=False,
        )
        if not p_id:
            return False
        # pylint: disable=consider-using-f-string
        with os.popen("%s | awk '{print $11}'" % ps_grep_v_str) as pro_name:
            p_name = pro_name.readlines()
        # pylint: disable=consider-using-f-string
        with os.popen("%s | awk '{print $12}'" % ps_grep_v_str) as pro_name_suffix:
            p_name_suffix = pro_name_suffix.readlines()

        if not p_name_suffix:
            logger.info(f"{app_name} start failed")

        logger.info(f"{app_name} | 进程查找结果为:{p_id}, {p_name}, {p_name_suffix}")
        return p_id, p_name, p_name_suffix

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
        command = os.popen(cmd_txt)
        result = command.read()
        command.close()
        if result:
            logger.debug(result)
            return True
        return False

    @classmethod
    def get_daemon_process_status(cls, app, grep_list: str = None) -> bool:
        """
         获取有守护进程的应用进程状态
        :param app: 应用包名
        :return: Boolean
        """
        if grep_list:
            cls.GREP_LIST = grep_list
        cmd = ""
        for i in cls.GREP_LIST:
            cmd += f"grep -v {i} | "
        cmd_txt = f"ps -aux | grep -v daemon | grep {app} | {cmd.rstrip('| ')}"
        logger.debug(cmd_txt)
        command = os.popen(cmd_txt)
        result = command.read()
        logger.debug(result)
        command.close()
        return bool(result)

    @classmethod
    def get_daemon_process_num(cls, app, grep_list: str = None) -> int:
        """
         获取有守护进程的应用进程数量
        :param app:
        :return: int
        """
        if grep_list:
            cls.GREP_LIST = grep_list
        cmd = ""
        for i in cls.GREP_LIST:
            cmd += f"grep -v {i} | "
        cmd_txt = f"ps -aux | grep -v daemon | grep {app} | {cmd.rstrip('| ')}"
        logger.debug(cmd_txt)
        command = os.popen(cmd_txt)
        result = command.read()
        command.close()
        logger.debug(result)
        num = len(result.split("\n")) - 1
        return num

    @staticmethod
    def minimize_current_window():
        """
         最小化当前激活窗口
        :return: None
        """
        with os.popen("xdotool windowminimize $(xdotool getactivewindow)"):
            pass

    @classmethod
    def change_sys_icon_theme(cls, theme="bloom"):
        """
         修改系统的图标主题
        :param theme: 默认 bloom. 支持：Vintage,bloom,bloom-classic,bloom-classic-dark,bloom-dark
        """
        logger.debug(f"设置系统图标主题为{theme}")
        cls.run_cmd(f'gsettings set com.deepin.xsettings icon-theme-name "{theme}"')

    @classmethod
    def change_app_to_default_theme(cls, app_name):
        """
         修改app主题跟随系统
        :param app_name: 应用名字
        """
        cls.run_cmd(
            f"gsettings set com.deepin.dtk:/dtk/deepin/{app_name}/ " "palette-type UnknownType"
        )

    @classmethod
    def kill_process(cls, process, grep_list: [list, tuple] = None):
        """
         杀进程
        :param process: 进程名
        """
        # 杀进程要过滤的进程
        if grep_list:
            cls.GREP_LIST = grep_list
        cmd = ""
        for i in cls.GREP_LIST:
            cmd += f"grep -v {i} | "
        os.system(f"ps -ef | grep {process} | {cmd}awk '{{print $2}}' | xargs kill -9 > /dev/null 2>&1")

    @classmethod
    def sudo_kill_process(cls, process, grep_list: [list, tuple] = None):
        if grep_list:
            cls.GREP_LIST = grep_list
        cmd = ""
        for i in cls.GREP_LIST:
            cmd += f"grep -v {i} | "
        from setting import conf
        os.system(
            f"process=$(ps -ef | grep {process} | {cmd}cut -c 9-15);echo '{conf.PASSWORD}' | sudo -S kill -9 $process > /dev/null 2>&1"
        )

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
