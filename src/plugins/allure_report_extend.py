# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114,C0103,R0903
import os
from tkinter import Tk
from functools import partial

from setting.globalconfig import GlobalConfig
from src.rtk._base import collect_result


def wf(f, t):
    f.write(t.encode("unicode_escape").decode() + "\n")


class AllureReportExtend:
    @staticmethod
    def environment_info(session, execute):
        try:
            allure_path = session.config.option.allure_report_dir
        except TypeError:
            return
        if not allure_path:
            return
        allure_fspath_path = os.path.join(
            session.config.invocation_dir, allure_path, "environment.properties"
        )
        with open(allure_fspath_path, "w+", encoding="utf-8") as _f:
            w = partial(wf, _f)

            py_case_info = ""
            if execute:
                total, failed, passed, skiped, _ = collect_result(execute)
                py_case_info = f"{total}/{passed}/{failed}/{skiped}"

            w(f"PMS用例维度(总数/通过/失败/跳过)={py_case_info}")
            w(f"网络地址={GlobalConfig.USERNAME}@{GlobalConfig.HOST_IP}")
            w(f"工作目录={GlobalConfig.ROOT_DIR}")
            w(f"镜像版本={GlobalConfig.VERSION}")

            screen = Tk()
            w(f"分辨率={screen.winfo_screenwidth()}x{screen.winfo_screenheight()}")
            w(f"显示协议={GlobalConfig.DISPLAY_SERVER.title()}")

            try:
                cpu_info = (
                    os.popen(
                        f"echo '{GlobalConfig.PASSWORD}' | sudo -S dmidecode -s  processor-version"
                    )
                    .readlines()[0]
                    .strip("\n")
                )
                w(f"CPU信息={cpu_info}")


                mem_info = os.popen(
                    f'''echo '{GlobalConfig.PASSWORD}' | sudo -S dmidecode|grep -A16 'Memory Device' | '''
                    'grep -v "Memory Device Mapped Address" | grep "Range Size"'
                ).readlines()
                MEM_TOTAL = sum([int(i.split(":")[1].rstrip(" GB\n").strip()) for i in mem_info])
                w(f"内存信息={MEM_TOTAL}G")
            except IndexError:
                ...

            os_info = os.popen("uname -a").read()
            w(f"内核信息={os_info}")
