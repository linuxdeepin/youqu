#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only

import json
import os
import re
import sys

from concurrent.futures import ALL_COMPLETED
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait

from time import sleep
from time import strftime

from allure_custom import AllureCustom
from allure_custom.conf import setting

from setting.globalconfig import GlobalConfig
from src.pms.send2pms import Send2Pms

setting.html_title = GlobalConfig.REPORT_TITLE
setting.report_name = GlobalConfig.REPORT_NAME
setting.report_language = GlobalConfig.REPORT_LANGUAGE

from src.cmdctl import CmdCtl
from src import logger
from src.rtk._base import Args
from src.rtk._base import transform_app_name
from setting import conf


class RemoteRunner:

    __author__ = "Mikigo <huangmingqiang@uniontech.com>"

    def __init__(
            self,
            remote_kwargs: dict = None,
            local_kwargs: dict = None,
    ):
        self.remote_kwargs = remote_kwargs
        self.local_kwargs = local_kwargs
        logger("INFO")
        self.parallel = conf.PARALLEL
        self.clean_server_report_dir = conf.CLEAN_SERVER_REPORT_DIR
        self.clean_client_report_dir = conf.CLEAN_CLIENT_REPORT_DIR
        self.send_code = conf.SEND_CODE
        self.scan = int(conf.SCAN)
        self.client_env = conf.BUILD_ENV
        self.client_password = conf.CLIENT_PASSWORD

        self._default = {
            Args.client_password.value: remote_kwargs.get("client_password")
                                        or self.client_password,
        }

        client_dict = {}
        _client = remote_kwargs.get("clients") or conf.CLIENTS
        if _client:
            clients = _client.split("/")
            for index, client in enumerate(clients):
                client_info = re.findall(r"^(.+?)@(\d+\.\d+\.\d+\.\d+):{0,1}(.*?)$", client)
                if client_info:
                    _c = list(client_info[0])
                    if _c[2] == "":
                        _c[2] = self._default.get(Args.client_password.value)
                    client_dict[f"client{index + 1}"] = _c

        else:
            raise ValueError(
                "未获取到测试机信息,请检查 setting/globalconfig.ini 中 CLIENT LIST 是否配置，"
                "或通过命令行 remote -c user@ip:password 传入。"
            )

        self.default = {
            Args.app_name.value: transform_app_name(
                local_kwargs.get("app_name") or GlobalConfig.APP_NAME
            ),
            Args.clients.value: client_dict,
            Args.send_code.value: remote_kwargs.get("send_code") or self.send_code,
            Args.build_env.value: remote_kwargs.get("build_env") or self.client_env,
            Args.parallel.value: remote_kwargs.get("parallel") or self.parallel,
            Args.json_backfill_base_url.value: remote_kwargs.get("json_backfill_base_url"),
            Args.json_backfill_task_id.value: remote_kwargs.get("json_backfill_task_id"),
            Args.json_backfill_user.value: remote_kwargs.get("json_backfill_user"),
            Args.json_backfill_password.value: remote_kwargs.get("json_backfill_password"),
            Args.json_backfill_custom_api.value: remote_kwargs.get("json_backfill_custom_api") or "api/youqu/yqresult/"
        }
        if "/home/" not in GlobalConfig.ROOT_DIR:
            raise EnvironmentError
        self.server_project_path = "/".join(GlobalConfig.ROOT_DIR.split("/")[3:])
        self.client_report_path = lambda x: f"/home/{x}/{self.server_project_path}/report"
        self.client_allure_report_path = (
            lambda
                x: f"/home/{x}/{self.server_project_path}/{GlobalConfig.report_cfg.get('ALLURE_REPORT_PATH', default='report')}/allure".replace(
                "//", "/"
            )
        )
        self.client_pms_json_report_path = (
            lambda x, y: f"/home/{x}/{self.server_project_path}/report/pms_{y}"
        )
        self.client_json_report_path = (
            lambda x: f"/home/{x}/{self.server_project_path}/report/json"
        )
        self.strf_time = strftime("%m%d%p%I%M%S")
        self.server_detail_json_path = f"{GlobalConfig.REPORT_PATH}/json/{self.strf_time}_remote"
        self.client_list = list(self.default.get(Args.clients.value).keys())
        _pty = "t"
        if len(self.client_list) >= 2:
            _pty = "T"
        self.ssh = f"sshpass -p '%s' ssh -{_pty}"
        self.scp = "sshpass -p '%s' scp -r"
        self.rsync = "sshpass -p '%s' rsync -av -e ssh"
        self.empty = "> /dev/null 2>&1"

        self.collection_json = False
        self.server_json_dir_id = None
        self.pms_user = None
        self.pms_password = None

    def send_code_to_client(self, user, _ip, password):
        logger.info(f"发送代码到测试机 - < {user}@{_ip} >")
        os.system(
            f"{self.ssh % password} {user}@{_ip} "
            f""""echo '{password}' | sudo -S rm -rf ~/Pipfile" {self.empty}"""
        )
        os.system(
            f"{self.ssh % password} {user}@{_ip} "
            f""""echo '{password}' | sudo -S rm -rf ~/{self.server_project_path}" {self.empty}"""
        )
        os.system(
            f'{self.ssh % password} {user}@{_ip} "mkdir -p ~/{self.server_project_path}" {self.empty}'
        )
        app_name: str = self.default.get(Args.app_name.value)
        exclude = ""
        for i in [
            "__pycache__",
            ".pytest_cache",
            ".vscode",
            ".idea",
            ".git",
            ".github",
            ".reuse",
            "docs",
            "node_modules",
            "report",
            ".gitignore",
            "CONTRIBUTING.md",
            "LICENSE",
            "package.json",
            "Pipfile",
            "Pipfile.lock",
            "pnpm-lock.yaml",
            "publish.sh",
            "pyproject.toml",
            "README.md",
            "RELEASE.md",
            "ruff.toml",
        ]:
            exclude += f"--exclude='{i}' "
        if app_name:
            for i in os.listdir(GlobalConfig.APPS_PATH):
                if i == "__init__.py":
                    continue
                if app_name.replace("-", "_") != i:
                    exclude += f"--exclude='{i}' "
        os.system(
            f"{self.rsync % (password,)} {exclude} {GlobalConfig.ROOT_DIR}/* "
            f"{user}@{_ip}:~/{self.server_project_path}/ {self.empty}"
        )
        os.system(
            f"{self.rsync % (password,)} {exclude} {GlobalConfig.ROOT_DIR}/.env "
            f"{user}@{_ip}:~/{self.server_project_path}/ {self.empty}"
        )

        logger.info(f"代码发送完成 - < {user}@{_ip} >")

    def build_client_env(self, user, _ip, password):
        logger.info(f"安装环境 - < {user}@{_ip} >")
        os.system(
            f"{self.ssh % password} {user}@{_ip} "
            f'''"rm -rf ~/.local/share/virtualenvs/{self.server_project_path.split('/')[-1]}*"'''
        )
        os.system(
            f"{self.ssh % password} {user}@{_ip} "
            f'"cd ~/{self.server_project_path}/ && bash env.sh -p {password}"'
        )
        logger.info(f"环境安装完成 - < {user}@{_ip} >")

    def send_code_and_env(self, user, _ip, password):
        self.send_code_to_client(user, _ip, password)
        self.build_client_env(user, _ip, password)

    def install_deb(self, user, _ip, password):
        logger.info(f"安装deb包 - < {user}@{_ip} >")
        os.system(
            f"{self.scp % password} {self.default.get(Args.deb_path.value)}/*.deb {user}@{_ip}:{self.default.get(Args.deb_path.value)}/"
        )
        os.system(
            f'''{self.ssh % password} {user}@{_ip} "cd {self.default.get(Args.deb_path.value)}/ && echo {password} | sudo -S dpkg -i *.deb"'''
        )
        logger.info(f"deb包安装完成 - < {user}@{_ip} >")

    def mul_do(self, func_obj, client_list):
        if len(client_list) >= 2:
            executor = ThreadPoolExecutor()
            _ps = []
            for client in client_list[:-1]:
                user, _ip, password = self.default.get(Args.clients.value).get(client)
                _p1 = executor.submit(func_obj, user, _ip, password)
                _ps.append(_p1)
            user, _ip, password = self.default.get(Args.clients.value).get(client_list[-1])
            func_obj(user, _ip, password)
            wait(_ps, return_when=ALL_COMPLETED)
        else:
            user, _ip, password = self.default.get(Args.clients.value).get(client_list[0])
            func_obj(user, _ip, password)

    def get_client_test_status(self, user, _ip, password):
        status_test = os.popen(
            f'{self.ssh % password} {user}@{_ip} "ps -aux | grep pytest | grep -v grep"'
        ).read()
        return bool(status_test)

    @staticmethod
    def make_dir(dirs):
        if not os.path.exists(dirs):
            os.makedirs(dirs)

    def run_pytest_cmd(self, user, _ip, password, outside_keywords=None):
        cmd = [
            self.ssh % password,
            f"{user}@{_ip}",
            '"',
            "cd",
        ]

        l_args = list(self.local_kwargs.items())
        real_app_name = ""
        _tmp_args = []
        for i in l_args:
            if i[1] is None:
                continue
            i = list(i)
            i[0] = f"--{i[0]}"
            i[1] = f"'{i[1]}'"
            if i[0] == "--app_name":
                real_app_name = f"apps/{self.default.get(Args.app_name.value)}"
                if self.default.get(Args.app_name.value) is None:
                    real_app_name = ""
                continue

            _tmp_args.extend(i)
        cmd.extend(
            [
                f"~/{self.server_project_path}/{real_app_name}",
                "&&",
                "pipenv",
                "run",
            ]
        )
        from src.rtk.local_runner import LocalRunner

        lr = LocalRunner(debug=True)
        lr_args = {k: v for k, v in lr.export_default.items() if v}
        rr_args = {k: v for k, v in self.local_kwargs.items() if v}
        lr_args.update(rr_args)
        if all(
                [
                    lr_args.get(Args.task_id.value),
                    lr_args.get(Args.pms_user.value),
                    lr_args.get(Args.pms_password.value),
                    lr_args.get(Args.send_pms.value) == "finish",
                ]
        ):
            lr_args[Args.trigger.value] = "hand"
            self.collection_json = True
            self.pms_user = lr_args.get(Args.pms_user.value)
            self.pms_password = lr_args.get(Args.pms_password.value)
            self.server_json_dir_id = lr_args.get(Args.task_id.value)
        pytest_cmd = lr.create_pytest_cmd(
            real_app_name.replace("apps/", ""),
            default=lr_args,
            proj_path=f"/home/{user}/{self.server_project_path}",
            outside_keywords=outside_keywords,
        )

        cmd.extend(pytest_cmd)
        cmd.append('"')
        cmd_str = " ".join(cmd)
        logger.info(f"\n{cmd_str}\n")
        if self.default.get(Args.debug.value):
            logger.info("DEBUG 模式不执行用例!")
        else:
            os.system(cmd_str)

    def collection_only_cmd(self, outside_keywords=None):
        app_dir = (
            self.default.get(Args.app_name.value) if self.default.get(Args.app_name.value) else ""
        )
        from src.rtk.local_runner import LocalRunner

        lr = LocalRunner(debug=True)
        lr_args = {k: v for k, v in lr.export_default.items() if v}
        rr_args = {k: v for k, v in self.local_kwargs.items() if v}
        lr_args.update(rr_args)
        if all(
                [
                    lr_args.get(Args.task_id.value),
                    lr_args.get(Args.pms_user.value),
                    lr_args.get(Args.pms_password.value),
                    lr_args.get(Args.send_pms.value) == "finish",
                ]
        ):
            lr_args[Args.trigger.value] = "hand"
            self.collection_json = True
            self.pms_user = lr_args.get(Args.pms_user.value)
            self.pms_password = lr_args.get(Args.pms_password.value)
            self.server_json_dir_id = lr_args.get(Args.task_id.value)
        cmd = lr.create_pytest_cmd(
            app_dir,
            default=lr_args,
            outside_keywords=outside_keywords,
        )
        cmd.append("--co")

        collect_only_cmd = " ".join(cmd)
        logger.info(f"Collecting: \n{collect_only_cmd}")
        collect_only_log = CmdCtl.run_cmd(collect_only_cmd)
        re_expr = re.compile(r"<Module (.*?)\.py>")
        cases = re.findall(re_expr, collect_only_log)
        if not cases:
            logger.error("未收集到用例")
            sys.exit(5)
        return cases

    def pre_env(self):
        os.system(f"rm -rf ~/.ssh/known_hosts {self.empty}")
        if self.clean_server_report_dir:
            os.system(f"rm -rf {GlobalConfig.REPORT_PATH}/* {self.empty}")
        if not self.default.get(Args.send_code.value) and self.clean_client_report_dir:
            for client in self.default.get(Args.clients.value):
                user, _ip, password = self.default.get(Args.clients.value).get(client)
                os.system(
                    f"""{self.ssh % password} {user}@{_ip} "rm -rf {self.client_report_path(user)}/*" {self.empty}"""
                )
        sudo = f"echo '{GlobalConfig.PASSWORD}' | sudo -S"
        if "StrictHostKeyChecking no" not in os.popen("cat /etc/ssh/ssh_config").read():
            os.system(
                f"""{sudo} sed -i "s/#   StrictHostKeyChecking ask/ StrictHostKeyChecking no/g" /etc/ssh/ssh_config {self.empty}"""
            )
        if "(C)" not in os.popen("sshpass -V").read():
            os.system(f"{sudo} apt update {self.empty}")
            os.system(f"{sudo} apt install sshpass {self.empty}")

    def scp_report(self, user, _ip, password):
        html_dir_endswith = f"_{self.default.get(Args.app_name.value)}" if self.default.get(Args.app_name.value) else ""
        if self.default.get(Args.parallel.value) == "no":
            self.nginx_server_allure_path = f"{GlobalConfig.REPORT_PATH}/allure/{self.strf_time}{html_dir_endswith}"
            self.make_dir(self.nginx_server_allure_path)
            status = os.system(
                f"{self.scp % password} {user}@{_ip}:{self.client_allure_report_path(user)}/* {self.nginx_server_allure_path}/ {self.empty}"
            )
            self.set_youqu_run_exitcode(status)
        else:
            server_allure_path = f"{GlobalConfig.REPORT_PATH}/allure/{self.strf_time}_ip{_ip}{html_dir_endswith}"
            self.make_dir(server_allure_path)
            status = os.system(
                f"{self.scp % password} {user}@{_ip}:{self.client_allure_report_path(user)}/* {server_allure_path}/ {self.empty}"
            )
            self.set_youqu_run_exitcode(status)
            if status == 0:
                generate_allure_html = f"{server_allure_path}/html"
                AllureCustom.gen(server_allure_path, generate_allure_html)

        if self.collection_json:
            server_json_path = f"{GlobalConfig.REPORT_PATH}/pms_{self.server_json_dir_id}/{self.strf_time}_ip{_ip}_{self.default.get(Args.app_name.value)}"
            self.make_dir(server_json_path)
            status = os.system(
                f"{self.scp % password} {user}@{_ip}:{self.client_pms_json_report_path(user, self.server_json_dir_id)}/* {server_json_path}/ {self.empty}"
            )
            self.set_youqu_run_exitcode(status)
        self.make_dir(self.server_detail_json_path)
        status = os.system(
            f"{self.scp % password} {user}@{_ip}:{self.client_json_report_path(user)}/detail_report.json {self.server_detail_json_path}/detail_report_{_ip}.json"
        )
        self.set_youqu_run_exitcode(status)
        status = os.system(
            f"{self.scp % password} {user}@{_ip}:{self.client_json_report_path(user)}/summarize.json {self.server_detail_json_path}/summarize_{_ip}.json"
        )
        self.set_youqu_run_exitcode(status)

    def set_youqu_run_exitcode(self, status):
        if status != 0:
            os.environ["YOUQU_RUN_EXIT_CODE"] = str(status)

    def exit_with_youqu_run_exitcode(self):
        youqu_run_exitcode = os.environ.get("YOUQU_RUN_EXIT_CODE")
        if youqu_run_exitcode is not None and int(youqu_run_exitcode) != 0:
            sys.exit(int(youqu_run_exitcode) >> 8)

    def remote_finish_send_to_pms(self):
        json_path = f"{GlobalConfig.REPORT_PATH}/pms_{self.server_json_dir_id}"
        self.make_dir(json_path)
        res = {}
        for root, dirs, files in os.walk(json_path):
            for file in files:
                if file.endswith(".json") and file != "total.json":
                    case_name = os.path.splitext(file)[0]
                    file_path = f"{root}/{file}"

                    with open(file_path, "r", encoding="utf-8") as f:
                        _client_res = json.load(f)
                    if not res.get(case_name):
                        res[case_name] = _client_res
                    else:
                        if res.get(case_name).get("result") != "fail":
                            res[case_name] = _client_res
        with open(f"{json_path}/total.json", "w+", encoding="utf-8") as f:
            f.write(json.dumps(res, indent=2, ensure_ascii=False))
        Send2Pms(
            user=self.pms_user,
            password=self.pms_password,
        ).remote_finish_push(res)

    def get_report(self, client_list):
        if len(self.default.get(Args.clients.value)) >= 2:
            _ps = []
            executor = ThreadPoolExecutor()
            for client in client_list[:-1]:
                user, _ip, password = self.default.get(Args.clients.value).get(client)
                _p4 = executor.submit(self.scp_report, user, _ip, password)
                _ps.append(_p4)
                sleep(2)
            user, _ip, password = self.default.get(Args.clients.value).get(client_list[-1])
            self.scp_report(user, _ip, password)
            wait(_ps, return_when=ALL_COMPLETED)
        else:
            user, _ip, password = self.default.get(Args.clients.value).get(client_list[0])
            self.scp_report(user, _ip, password)

        if self.collection_json:
            self.remote_finish_send_to_pms()
        if all([
            self.default.get(Args.json_backfill_base_url.value),
            self.default.get(Args.json_backfill_task_id.value),
            self.default.get(Args.json_backfill_user.value),
            self.default.get(Args.json_backfill_password.value),
            self.default.get(Args.json_backfill_custom_api.value)
        ]):
            from src.rtk.json_backfill import JsonBackfill
            try:
                JsonBackfill(
                    base_url=self.default.get(Args.json_backfill_base_url.value),
                    username=self.default.get(Args.json_backfill_user.value),
                    password=self.default.get(Args.json_backfill_password.value),
                    custom_api=self.default.get(Args.json_backfill_custom_api.value),
                ).remote_backfill(self.server_detail_json_path, self.default.get(Args.json_backfill_task_id.value))
            except Exception as e:
                logger.error(e)
                sys.exit(1)
        if self.default.get(Args.parallel.value) == "no":
            summarize = {
                "total": 0,
                "pass": 0,
                "fail": 0,
                "skip": 0,
            }
            for file in os.listdir(self.server_detail_json_path):
                if file.startswith("summarize_") and file.endswith(".json"):
                    with open(f"{self.server_detail_json_path}/{file}", "r", encoding="utf-8") as f:
                        res = json.load(f)
                    for i in summarize.keys():
                        summarize[i] += res.get(i)
            with open(f"{self.server_detail_json_path}/summarize.json", "w", encoding="utf-8") as _f:
                _f.write(json.dumps(summarize, indent=2, ensure_ascii=False))

            generate_allure_html = f"{self.nginx_server_allure_path}/html"
            AllureCustom.gen(self.nginx_server_allure_path, generate_allure_html)

    def parallel_run(self, client_list, client_cases_map=None):
        if client_cases_map is None:
            client_cases_map = {}
        _ps = []
        executor = ThreadPoolExecutor()
        for client in client_list[:-1]:
            user, _ip, password = self.default.get(Args.clients.value).get(client)
            _p3 = executor.submit(self.run_pytest_cmd, user, _ip, password, client_cases_map.get(client))
            _ps.append(_p3)
            sleep(1)
        user, _ip, password = self.default.get(Args.clients.value).get(client_list[-1])
        self.run_pytest_cmd(
            user,
            _ip,
            password,
            client_cases_map.get(client_list[-1])
        )
        wait(_ps, return_when=ALL_COMPLETED)
        sleep(5)

    def remote_run(self):
        client_list = list(self.default.get(Args.clients.value).keys())
        self.pre_env()
        logger.info(
            "\n测试机列表:\n"
            + "\n".join([str(i) for i in self.default.get(Args.clients.value).items()])
        )
        if self.default.get(Args.build_env.value):
            self.mul_do(self.send_code_and_env, client_list)
        else:
            if self.default.get(Args.send_code.value):
                self.mul_do(self.send_code_to_client, client_list)
        if self.default.get(Args.deb_path.value):
            self.mul_do(self.install_deb, client_list)
        if self.default.get(Args.parallel.value) == "no":
            case_files = self.collection_only_cmd()
            logger.info(f"Collected {len(case_files)} case.")

            def split_case(lst, n):
                k, m = divmod(len(lst), n)
                return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

            split_case_files = split_case(case_files, len(client_list))
            client_cases_map = dict(zip(client_list, split_case_files))
            self.parallel_run(client_list, client_cases_map)
        else:
            self.parallel_run(client_list)
        self.get_report(client_list)
        self.exit_with_youqu_run_exitcode()
