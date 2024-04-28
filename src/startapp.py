#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114,C0115,C0116,R1722,W1514,C0103,W1514,C0103,R1721,R0912,W0612
import os
import re
import shutil
from time import strftime
from configparser import ConfigParser

from setting.globalconfig import GlobalConfig
from setting.globalconfig import FixedCsvTitle


class StartApp:
    def __init__(self, app_name: str):
        self.app_name = app_name.strip("/")

    def copy_template_to_apps(self):
        """copy_template_to_apps"""
        app_name_path = f"{GlobalConfig.APPS_PATH}/{self.app_name}"
        if os.path.exists(app_name_path) and os.listdir(app_name_path):
            if input(
                f"{GlobalConfig.APPS_PATH}/{self.app_name}目录存在且里面存在文件，请确认是否清空（Y/N）："
            ) in ("y", "Y"):
                os.system(f"rm -rf {app_name_path}/*")
            else:
                exit(0)
        if not os.path.exists(app_name_path):
            os.makedirs(app_name_path)
        os.system(
            "cp -r " f"{GlobalConfig.SETTING_PATH}/template/app_template/* " f"{app_name_path}/"
        )
        os.system(
            "cp -r "
            f"{GlobalConfig.SETTING_PATH}/template/app_template/.gitignore-tpl "
            f"{app_name_path}/"
        )

    def rewrite(self):
        """rewrite"""
        for root, dirs, files in os.walk(f"{GlobalConfig.APPS_PATH}/{self.app_name}"):
            for file in files:
                app_name = self.app_name
                if self.app_name.startswith("autotest_"):
                    app_name = re.sub(r"autotest_", "", self.app_name)

                if file.endswith("-tpl"):
                    shutil.move(f"{root}/{file}", f"{root}/{file[:-4]}")
                    file = file[:-4]

                if "${app_name}" in file:
                    new_file = re.sub(
                        r"\${app_name}", app_name if app_name else self.app_name, file
                    )
                    shutil.move(f"{root}/{file}", f"{root}/{new_file}")
                    file = new_file

                if ".py" in file or ".csv" in file:
                    with open(f"{root}/{file}", "r") as f:
                        codes = f.readlines()
                    new_codes = []
                    for code in codes:
                        if "##" in code:
                            code = code.replace("##", "")
                        if "${APP_NAME}" in code:
                            code = re.sub(r"\${APP_NAME}", self.app_name, code)
                        if "${app_name}" in code:
                            code = re.sub(r"\${app_name}", app_name, code)
                        if "${APP-NAME}" in code:
                            code = re.sub(r"\${APP-NAME}", app_name.replace("_", "-"), code)
                        if "${AppName}" in code:
                            code = re.sub(r"\${AppName}", app_name.title().replace("_", ""), code)
                        if "${USER}" in code:
                            code = re.sub(r"\${USER}", GlobalConfig.USERNAME, code)
                        if "${DATE}" in code:
                            code = re.sub(r"\${DATE}", strftime("%Y/%m/%d"), code)
                        if "${TIME}" in code:
                            code = re.sub(r"\${TIME}", strftime("%H:%M:%S"), code)
                        if "${FIXEDCSVTITLE}" in code:
                            code = re.sub(
                                r"\${FIXEDCSVTITLE}",
                                ",".join([i.value for i in FixedCsvTitle]),
                                code,
                            )
                        new_codes.append(code)
                    with open(f"{root}/{file}", "w") as f:
                        f.writelines([i for i in new_codes])

                if file == "control":
                    conf = ConfigParser()
                    conf.read(f"{root}/{file}")
                    conf.set("Depends", "autotest-basic-frame", GlobalConfig.current_tag)
                    with open(f"{root}/{file}", "w", encoding="utf-8") as f:
                        conf.write(f)

        print(f"{self.app_name} 创建成功,请查看 {GlobalConfig.APPS_PATH}/{self.app_name}")
