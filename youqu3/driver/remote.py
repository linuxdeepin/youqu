#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import os
import pathlib
import re
import socket
from concurrent.futures import ALL_COMPLETED
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
from copy import deepcopy

from youqu3 import logger
from youqu3 import setting
from youqu3 import sleep
from youqu3.cmd import Cmd, RemoteCmd


class Remote:
    __author__ = "mikigo <huangmingqiang@uniontech.com>"

    def __init__(
            self,
            clients=None,
            workdir=None,
            path=None,
            keywords=None,
            tags=None,
            slaves=None,
            txt=None,
            reruns=None,
            job_start=None,
            job_end=None,
            pytest_opt=None,
            record_failed_num=None,
            **kwargs
    ):
        logger("INFO")

        self.workdir = workdir
        self.path = path
        self.keywords = keywords
        self.tags = tags
        self.clients = clients
        self.slaves = slaves
        self.txt = txt
        self.reruns = reruns
        self.job_start = job_start
        self.job_end = job_end
        self.pytest_opt = pytest_opt
        self.record_failed_num = record_failed_num

        if not self.clients:
            raise ValueError("REMOTE驱动模式, 未传入远程客户端信息：-c/--clients user@ip:pwd")
        self.group_type = False
        if "{" in self.clients and "}" in self.clients:
            self.group_type = True

        if self.group_type is False:
            self.cli_clients = {}
            _cli_clients = self.clients.split("/")
            for index, _client in enumerate(_cli_clients):
                _cli_client_info = re.findall(r"^(.+?)@(\d+\.\d+\.\d+\.\d+):{0,1}(.*?)$", _client)
                if _cli_client_info:
                    _c = list(_cli_client_info[0])
                    if _c[2] == "":
                        _c[2] = setting.PASSWORD
                    connected = self.check_remote_connected(*_c)
                    self.cli_clients[f"client{index + 1}{f'' if connected else '-X'}"] = _c
        else:
            self.cli_groups = {}
            groups = re.findall(r'\{(.*?)\}', self.clients)
            for group_index, group in enumerate(groups):
                cli_clients = {}
                for client_index, _client in enumerate(group.split("/")):
                    _cli_client_info = re.findall(r"^(.+?)@(\d+\.\d+\.\d+\.\d+):{0,1}(.*?)$", _client)
                    if _cli_client_info:
                        _c = list(_cli_client_info[0])
                        if _c[2] == "":
                            _c[2] = setting.PASSWORD
                        connected = self.check_remote_connected(*_c)
                        cli_clients[f"client{client_index + 1}{f'' if connected else '-X'}"] = _c
                self.cli_groups[f"group{group_index + 1}"] = cli_clients

        self.server_rootdir = pathlib.Path(".").absolute()
        self.rootdir_name = self.server_rootdir.name
        self.client_rootdir = lambda x: f"/home/{x}/{self.rootdir_name}_{setting.TIME_STRING}"
        self.client_report_path = lambda x: f"{self.client_rootdir(x)}/report"
        self.client_html_report_path = lambda x: f"{self.client_report_path(x)}/html"
        self.client_json_report_path = lambda x: f"{self.client_report_path(x)}/json"

        self.rsync = 'rsync -av -e "ssh -o StrictHostKeyChecking=no"'
        self.empty = "> /dev/null 2>&1"

        self.collection_json = False
        self.server_json_dir_id = None
        self.inside_filepath = None

        from funnylog2.config import config as funnylog2_config
        funnylog2_config.LOG_FILE_PATH = self.server_rootdir

    def check_remote_connected(self, user, _ip, password):
        logger.info(f"Checking remote: {user, _ip, password}")
        try:
            _, return_code = RemoteCmd(user, _ip, password).remote_run("hostname -I", return_code=True, timeout=1)
            if return_code == 0:
                return True
            return False
        except socket.timeout:
            return False

    def send_code(self, user, _ip, password):
        logger.info(f"开始发送代码到测试机 - < {user}@{_ip} >")
        RemoteCmd(user, _ip, password).remote_sudo_run(f"rm -rf {self.client_rootdir(user)}")
        RemoteCmd(user, _ip, password).remote_run(f"mkdir -p {self.client_rootdir(user)}")
        exclude = ""
        for i in [
            "__pycache__",
            ".pytest_cache",
            ".vscode",
            ".idea",
            ".git",
            ".github",
            ".venv",
            "report",
            ".gitignore",
            "LICENSE",
            "Pipfile",
            "Pipfile.lock",
            "README.md",
        ]:
            exclude += f"--exclude='{i}' "
        _, return_code = Cmd.expect_run(
            f"/bin/bash -c '{self.rsync} {exclude} {self.server_rootdir}/* {user}@{_ip}:{self.client_rootdir(user)}/'",
            events={'password': f'{password}\n'},
            return_code=True
        )
        a, return_code = Cmd.expect_run(
            f"/bin/bash -c '{self.rsync} {self.server_rootdir}/.env {user}@{_ip}:{self.client_rootdir(user)}/'",
            events={'password': f'{password}\n'},
            return_code=True
        )
        logger.info(f"代码发送{'成功' if return_code == 0 else '失败'} - < {user}@{_ip} >")

    def install_client_env(self, user, _ip, password):
        logger.info(f"开始安装环境 - < {user}@{_ip} >")

        def _remote_run(cmd):
            return RemoteCmd(user, _ip, password).remote_run(cmd, return_code=True)

        _, return_code = _remote_run("pip3 --version")
        if return_code != 0:
            _remote_run("curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py")
        _remote_run(f"pip3 install -U youqu3 -i {setting.PYPI_MIRROR}")
        _, return_code = _remote_run(
            f"export PATH=$PATH:$HOME/.local/bin;cd {self.client_rootdir(user)} && youqu3 envx")
        logger.info(f"环境安装{'成功' if return_code == 0 else '失败'} - < {user}@{_ip} >")

    def send_code_and_env(self, user, _ip, password):
        self.send_code(user, _ip, password)
        self.install_client_env(user, _ip, password)

    @staticmethod
    def makedirs(dirs):
        pathlib.Path(dirs).mkdir(parents=True, exist_ok=True)

    def get_back_report(self, user, _ip, password):
        server_html_path = f"{self.server_rootdir}/report/remote/{setting.TIME_STRING}_{_ip}_{self.rootdir_name}"
        self.makedirs(server_html_path)
        Cmd.expect_run(
            f"/bin/bash -c '{self.rsync} {user}@{_ip}:{self.client_report_path(user)}/* {server_html_path}/'",
            events={'password': f'{password}\n'},
            return_code=True
        )

    def get_back_all_report(self, client_list, clients):

        if len(clients) >= 2:
            _ps = []
            executor = ThreadPoolExecutor()
            for client in client_list[:-1]:
                user, _ip, password = clients.get(client)
                _p4 = executor.submit(self.get_back_report, user, _ip, password)
                _ps.append(_p4)
                sleep(2)
            user, _ip, password = clients.get(client_list[-1])
            self.get_back_report(user, _ip, password)
            wait(_ps, return_when=ALL_COMPLETED)
        else:
            user, _ip, password = clients.get(client_list[0])
            self.get_back_report(user, _ip, password)

    def read_tags_txt(self):
        youqu_tags_file = os.path.join(self.server_rootdir, "youqu-tags.txt")
        if os.path.exists(youqu_tags_file):
            with open(youqu_tags_file, "r", encoding="utf-8") as f:
                tags_txt = f.readlines()[0]
                return tags_txt
        return None

    def read_keywords_txt(self):
        youqu_keywords_file = os.path.join(self.server_rootdir, "youqu-keywords.txt")
        if os.path.exists(youqu_keywords_file):
            with open(youqu_keywords_file, "r", encoding="utf-8") as f:
                keywords_txt = f.readlines()[0]
                return keywords_txt
        return None

    def changedir_remote_cmd(self, user):
        return [
            "export PATH=$PATH:$HOME/.local/bin;",
            "cd",
            f"{self.client_rootdir(user)}/",
            "&&",
        ]

    @property
    def generate_cmd(self):
        cmd = ["youqu3-cargo", "run"]

        if self.workdir:
            if os.path.exists(self.workdir):
                cmd.extend(["--workdir", self.workdir])
            else:
                raise FileNotFoundError(f"workdir not found: {self.workdir}")
        if self.path:
            cmd.append(f"'{self.path}'")
        if self.inside_filepath:
            cmd.append(f"'{self.inside_filepath}'")

        keywords_txt = self.read_keywords_txt()
        if self.keywords:
            cmd.extend(["-k", f"'{self.keywords}'"])
        elif self.txt and keywords_txt is not None:
            cmd.extend(["-k", f"'{keywords_txt}'"])

        tags_txt = self.read_tags_txt()
        if self.tags:
            cmd.extend(["-m", f"'{self.tags}'"])
        elif self.txt and tags_txt is not None:
            cmd.extend(["-m", f"'{tags_txt}'"])
        if self.slaves:
            cmd.extend(["--slaves", f"'{self.slaves}'"])
        if self.reruns:
            cmd.extend(["--reruns",self.reruns])
        if self.job_start:
            cmd.extend(["--job-start",f"'{self.job_start}'"])
        if self.job_end:
            cmd.extend(["--job-end",f"'{self.job_end}"])
        if self.pytest_opt:
            cmd.extend([i.strip() for i in self.pytest_opt])
        if self.record_failed_num or setting.RECORD_FAILED_NUM:
            cmd.extend(["--record_failed_num", f"{self.record_failed_num or setting.RECORD_FAILED_NUM}"])
        return cmd

    def run_test(self, user, _ip, password):
        RemoteCmd(user, _ip, password).remote_run(
            " ".join(
                self.changedir_remote_cmd(user) + self.generate_cmd
            )
        )

    @property
    def collection_only_cmd(self):
        return self.generate_cmd + ["--setup-plan"]

    @property
    def get_collection_only_cases(self):
        stdout = Cmd.run(f"cd {self.server_rootdir} && {' '.join(self.collection_only_cmd)}", timeout=600)
        lines = stdout.split("\n")
        _collection_cases = []
        for line in lines:
            line = line.strip()
            if line and " " not in line:
                _collection_cases.append(line.split("::")[0])
        collection_cases = set(_collection_cases)
        return collection_cases

    def parallel_run(self, client_name_list, clients):
        _ps = []
        executor = ThreadPoolExecutor()
        all_clients_name_list = deepcopy(list(clients.keys()))
        for i in all_clients_name_list:
            if i not in client_name_list:
                clients.pop(i)
        for client in list(clients.keys())[:-1]:
            user, _ip, password = clients.get(client)
            _p3 = executor.submit(self.run_test, user, _ip, password)
            _ps.append(_p3)
            sleep(1)
        user, _ip, password = list(clients.values())[-1]
        self.run_test(user, _ip, password)
        wait(_ps, return_when=ALL_COMPLETED)
        sleep(5)

    def mul_do(self, func_obj, client_list, clients):
        if len(client_list) >= 2:
            executor = ThreadPoolExecutor()
            _ps = []
            for client in client_list[:-1]:
                user, _ip, password = clients.get(client)
                _p1 = executor.submit(func_obj, user, _ip, password)
                _ps.append(_p1)
            user, _ip, password = clients.get(client_list[-1])
            func_obj(user, _ip, password)
            wait(_ps, return_when=ALL_COMPLETED)
        else:
            user, _ip, password = clients.get(client_list[0])
            func_obj(user, _ip, password)

    def run(self):
        Cmd.run(f"rm -rf ~/.ssh/known_hosts {self.empty}")

        if self.group_type:
            print("┏" + "━" * 56 + "┓")
            print("┃" + "YOUQU3 REMOTE DRIVER".center(56) + "┃")
            print("┣" + "━" * 56 + "┫")
            print(
                f"┃{'GROUPS'.center(8)}┃{'CLIENTS'.center(9)}┃{'USER'.center(10)}┃{'IP'.center(15)}┃{'PASSWORD'.center(10)}┃")
            for group, clients in self.cli_groups.items():
                print("┣" + "━" * 56 + "┫")
                for c, (user, _ip, password) in clients.items():
                    print(f"┃{group.center(8)}┃{c.center(9)}┃{user.center(10)}┃{_ip.center(15)}┃{password.center(10)}┃")
            print("┗" + "━" * 56 + "┛")

            def split_case(lst, n):
                k, m = divmod(len(lst), n)
                return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

            task = []
            collection_cases = self.get_collection_only_cases
            executor = ThreadPoolExecutor()
            for group, clients in self.cli_groups.items():
                _client_name_list = list(clients.keys())
                client_name_list = [i for i in _client_name_list if not i.endswith("-X")]
                if len(client_name_list) > 1:
                    client_cases_map = dict(
                        zip(client_name_list, split_case(list(collection_cases), len(client_name_list)))
                    )
                    for client_name in client_name_list:
                        # self.group_client_worker(client_cases_map, client_name, clients)
                        t = executor.submit(self.group_client_worker, client_cases_map, client_name, clients)
                        task.append(t)

                else:
                    if client_name_list:
                        # self.client_worker(client_name_list, clients)
                        t = executor.submit(self.client_worker, client_name_list, clients)
                        task.append(t)

            wait(task, return_when=ALL_COMPLETED)

        else:
            print("┏" + "━" * 47 + "┓")
            print("┃" + "YOUQU3 REMOTE DRIVER".center(47) + "┃")
            print("┣" + "━" * 47 + "┫")
            print(f"┃{'CLIENTS'.center(9)}┃{'USER'.center(10)}┃{'IP'.center(15)}┃{'PASSWORD'.center(10)}┃")
            print("┣" + "━" * 47 + "┫")
            for c, (user, _ip, password) in self.cli_clients.items():
                print(f"┃{c.center(9)}┃{user.center(10)}┃{_ip.center(15)}┃{password.center(10)}┃")
            print("┗" + "━" * 47 + "┛")

            _client_name_list = list(self.cli_clients.keys())
            client_name_list = [i for i in _client_name_list if not i.endswith("-X")]
            self.mul_do(self.send_code_and_env, client_name_list, self.cli_clients)
            self.parallel_run(client_name_list, self.cli_clients)
            self.get_back_all_report(client_name_list, self.cli_clients)

    def client_worker(self, client_name_list, clients):
        client_info = clients.get(client_name_list[0])
        self.send_code_and_env(*client_info)
        self.run_test(*client_info)
        self.get_back_report(*client_info)

    def group_client_worker(self, client_cases_map, client_name, clients):
        client_info = clients.get(client_name)
        client_cases = client_cases_map.get(client_name)
        self.inside_filepath = " ".join(client_cases)
        self.send_code_and_env(*client_info)
        self.run_test(*client_info)
        self.get_back_report(*client_info)
