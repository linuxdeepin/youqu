#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
from setting import conf
from src.read_toml import read_toml
from src.rtk.local_runner import LocalRunner
from src.rtk.remote_runner import RemoteRunner


class PlayBook:
    def __init__(self, cli_kwargs):
        cli_url = cli_kwargs.get("url")
        cli_branch_or_tag = cli_kwargs.get("branch")
        cli_user = cli_kwargs.get("user")
        cli_password = cli_kwargs.get("password")
        cli_depth = cli_kwargs.get("depth")
        cli_path_to = cli_kwargs.get("path_to")
        cli_execution_mode = cli_kwargs.get("execution_mode")
        cli_clients = cli_kwargs.get("clients")
        cli_slaves = cli_kwargs.get("slaves")
        cli_keywords = cli_kwargs.get("keywords")
        cli_tags = cli_kwargs.get("tags")
        cli_pms_case_file_path = cli_kwargs.get("pms_case_file_path")

        ts = read_toml(f"{conf.SETTING_PATH}/playbook.toml")
        if cli_url:
            self.git_clone(
                cli_url, cli_user, cli_password, cli_branch_or_tag, cli_path_to, cli_depth
            )
        else:
            cfg_repos = ts.get("repositories")
            for cfg_repo in cfg_repos:
                cfg_url = cfg_repo.get("url")
                cfg_branch_or_tag = cfg_repo.get("branch_or_tag")
                cfg_depth = cfg_repo.get("depth")
                cfg_path_to = cfg_repo.get("path_to")
                cfg_user = cfg_repo.get("user")
                cfg_password = cfg_repo.get("password")
                self.git_clone(
                    cfg_url, cfg_user, cfg_password, cfg_branch_or_tag, cfg_path_to, cfg_depth
                )

        cfg_play = ts.get("play")
        cfg_execution_mode = cfg_play.get("execution_mode")
        cfg_clients = cfg_play.get("clients")
        cfg_slaves = cfg_play.get("slaves")
        cfg_keywords = cfg_play.get("keywords")
        cfg_tags = cfg_play.get("tags")
        cfg_pms_case_file_path = cfg_play.get("pms_case_file_path")

        kwargs = {
            "execution_mode": cli_execution_mode or cfg_execution_mode,
            "clients": cli_clients or cfg_clients,
            "slaves": cli_slaves or cfg_slaves,
            "keywords": cli_keywords or cfg_keywords,
            "tags": cli_tags or cfg_tags,
            "pms_case_file_path": cli_pms_case_file_path or cfg_pms_case_file_path,
        }

        self.playbook(kwargs)

    def git_clone(self, url, user, password, branch_or_tag, path_to, depth):
        if user and password:
            from src.git.clone import sslclone

            sslclone(url, user, password, branch_or_tag, path_to, depth)
        else:
            from src.git.clone import clone

            clone(url, branch_or_tag, path_to, depth)

    def playbook(self, kwargs):
        execution_mode = kwargs.get("execution_mode")
        if execution_mode not in ["run", "remote"]:
            raise ValueError
        if execution_mode == "remote":
            RemoteRunner(**kwargs).remote_run()
        else:
            LocalRunner(**kwargs).local_run()
