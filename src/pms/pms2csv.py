#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
# pylint: disable=C0301,C0115,R0903,C0103,C0201,R1710,R0914,W1514,R0914,R1702
import json
import os
from configparser import ConfigParser

from setting.globalconfig import FixedCsvTitle
from setting.globalconfig import GetCfg
from setting.globalconfig import GlobalConfig
from src import logger
from src.pms._base import MAX_CASE_NUMBER
from src.pms._base import _Base
from src.pms._base import _unicode_to_cn
from src.rtk._base import transform_app_name


class Pms2Csv(_Base):
    """获取pms数据同步到本地csv文件"""

    __author__ = "mikigo<huangmingqiang@uniontech.com>"

    config_error_log = "请检查您传递的 '命令行参数' 或 setting/globalconfig.ini 里的配置项"

    def __init__(self, app_name=None, user=None, password=None, pms_link_csv=None):
        super().__init__(user=user, password=password)
        self.walk_dir = (
            f"{GlobalConfig.APPS_PATH}/{transform_app_name(app_name)}"
            if app_name
            else GlobalConfig.APPS_PATH
        )

        conf = ConfigParser()
        conf.read(GlobalConfig.GLOBAL_CONFIG_FILE_PATH)
        ini_csv_names = conf.options("pmsctl-pms_link_csv")
        ini_csv_pms_map = GetCfg(GlobalConfig.GLOBAL_CONFIG_FILE_PATH, "pmsctl-pms_link_csv")
        cli_csv_pms_map = {}
        cli_csv_names = []
        if pms_link_csv:
            _cli_csv_names = pms_link_csv.split("/")
            for i in _cli_csv_names:
                pls = i.split(":")
                if len(pls) != 2:
                    raise ValueError("--pms_link_csv 参数的值可能有问题")
                csv_name, pms_product_id = pls
                cli_csv_names.append(csv_name.strip())
                cli_csv_pms_map[csv_name.strip()] = pms_product_id.strip()

        self.csv_names = cli_csv_names or ini_csv_names
        self.csv_link_cfg = cli_csv_pms_map or ini_csv_pms_map

        if not self.csv_names:
            raise ValueError(self.config_error_log)

        self.pms_mark = GetCfg(f"{GlobalConfig.SETTING_PATH}/pmsmark.ini", "pms-mark-to-csv-mark")

    def get_data_from_pms(self, app_case_id):
        """获取pms上数据"""
        if not app_case_id:
            raise ValueError(self.config_error_log)
        case_url = (
            f"https://pms.uniontech.com/{GlobalConfig.CASE_FROM}-browse-"
            f'{app_case_id}-{"-" if GlobalConfig.CASE_FROM == "testcase" else ""}all-0-id_desc-0-{MAX_CASE_NUMBER}.json'
        )
        res = self.rx.open_url(case_url, timeout=10)
        try:
            res_dict = json.loads(res)
        except json.decoder.JSONDecodeError:
            logger.error(f"获取pms数据失败, {self.config_error_log}")
            return

        cases = json.loads(res_dict["data"]).get("cases")
        res_data = {}
        for i in cases:
            case = cases.get(i)
            case_id = case.get("id")
            case_level = case.get("pri")
            case_type = self.pms_mark.get(case.get("type"))
            case_from = case.get("caseSource")
            device_type = case.get("deviceType")
            online_obj = case.get("lineCD")
            # if case_type:
            res_data[case_id] = {
                "case_level": f"L{case_level}",
                "case_type": case_type,
                "case_from": "BUG" if case_from == "是" else "",
                "device_type": device_type.split("(")[0]
                if device_type and device_type != "null"
                else "",
                "online_obj": "CICD" if online_obj == "是" else "",
                "skip_reason": "skip-下线CD" if online_obj == "否" else None,
            }
        if not res_data:
            logger.error(f"未从pms获取到数据, {self.config_error_log}")
            raise ValueError
        return res_data

    def read_csv(self):
        """读取本地csv文件数据"""
        csv_path_dict = {}
        csv_bak_path = f"{GlobalConfig.REPORT_PATH}/pms2csv_back"
        if not os.path.exists(csv_bak_path):
            os.makedirs(csv_bak_path)
        for root, _, files in os.walk(self.walk_dir):
            for file in files:
                if file.endswith(".csv") and os.path.splitext(file)[0] in self.csv_names:
                    csv_path_dict[os.path.splitext(file)[0]] = f"{root}/{file}"
                    os.system(f"cp {root}/{file} {csv_bak_path}/{GlobalConfig.TIME_STRING}_{file}")
        if not csv_path_dict:
            raise ValueError(f"{self.walk_dir} 目录下未找对应的到csv文件，{self.config_error_log}")

        res_tags = {}
        csv_heads_dict = {}
        for csv_name in csv_path_dict:
            with open(csv_path_dict.get(csv_name), "r", encoding="utf-8") as f:
                txt_list = f.readlines()
            csv_heads = txt_list[0].strip().split(",")

            csv_head_index_map = {}
            for index, title in enumerate(csv_heads):
                for i in FixedCsvTitle:
                    if i.value == title.strip():
                        csv_head_index_map[i.name] = {
                            "head_name": i.value,
                            "head_index": index,
                        }

            taglines = [txt.strip().split(",") for txt in txt_list[1:]]
            id_tags_dict = {i[0]: i for i in taglines if i[0]}
            res_tags[csv_name] = id_tags_dict
            csv_heads_dict[csv_name] = csv_head_index_map
        return res_tags, csv_heads_dict, csv_path_dict

    def compare_pms_to_csv(self):
        """对比pms上数据和本地csv文件数据"""
        (res_tags, csv_heads_dict, csv_path_dict) = self.read_csv()
        new_csv_file_tags = {}
        for csv_name in res_tags:
            product_id = self.csv_link_cfg.get(csv_name)
            pms_tags_dict = self.get_data_from_pms(product_id)
            if pms_tags_dict is None:
                continue
            logger.info(f"csv_name: {csv_name}")
            logger.info(f"product_id: {product_id}")
            csv_tags_dict = res_tags.get(csv_name)
            csv_head_dict = csv_heads_dict.get(csv_name)

            pms_case_id_index = case_level_index = case_type_index = None
            case_from_index = device_type_index = online_obj_index = None
            skip_reason_index = None

            pms_case_id_name = csv_head_dict.get(FixedCsvTitle.pms_case_id.name)
            if pms_case_id_name:
                pms_case_id_index = pms_case_id_name.get("head_index")

            case_level_name = csv_head_dict.get(FixedCsvTitle.case_level.name)
            if case_level_name:
                case_level_index = case_level_name.get("head_index")

            case_type_name = csv_head_dict.get(FixedCsvTitle.case_type.name)
            if case_type_name:
                case_type_index = case_type_name.get("head_index")

            case_from_name = csv_head_dict.get(FixedCsvTitle.case_from.name)
            if case_from_name:
                case_from_index = case_from_name.get("head_index")

            device_type_name = csv_head_dict.get(FixedCsvTitle.device_type.name)
            if device_type_name:
                device_type_index = device_type_name.get("head_index")

            online_obj_name = csv_head_dict.get(FixedCsvTitle.online_obj.name)
            if online_obj_name:
                online_obj_index = online_obj_name.get("head_index")

            skip_reason_name = csv_head_dict.get(FixedCsvTitle.skip_reason.name)
            if skip_reason_name:
                skip_reason_index = skip_reason_name.get("head_index")

            new_csv_tags = []
            new_csv_tags.append([i.get("head_name") for i in list(csv_head_dict.values())])
            for csv_case_id in csv_tags_dict:
                for pms_case_id in pms_tags_dict:
                    if pms_case_id == csv_case_id:
                        pms_tags = pms_tags_dict.get(pms_case_id)
                        case_level = pms_tags.get("case_level")
                        case_type = pms_tags.get("case_type")
                        case_from = pms_tags.get("case_from")
                        device_type = pms_tags.get("device_type")
                        online_obj = pms_tags.get("online_obj")
                        skip_reason = pms_tags.get("skip_reason")
                        flag = False
                        if (
                            pms_case_id_index
                            and csv_tags_dict[csv_case_id][pms_case_id_index] != pms_case_id
                        ):
                            csv_tags_dict[csv_case_id][pms_case_id_index] = pms_case_id
                            flag = True
                        if (
                            case_level_index
                            and csv_tags_dict[csv_case_id][case_level_index] != case_level
                        ):
                            csv_tags_dict[csv_case_id][case_level_index] = case_level
                            flag = True
                        if (
                            case_type_index
                            and csv_tags_dict[csv_case_id][case_type_index] != case_type
                        ):
                            csv_tags_dict[csv_case_id][case_type_index] = case_type
                            flag = True
                        if (
                            case_from_index
                            and csv_tags_dict[csv_case_id][case_from_index] != case_from
                        ):
                            csv_tags_dict[csv_case_id][case_from_index] = case_from
                            flag = True
                        if (
                            device_type_index
                            and csv_tags_dict[csv_case_id][device_type_index] != device_type
                        ):
                            csv_tags_dict[csv_case_id][device_type_index] = device_type
                            flag = True
                        if (
                            online_obj_index
                            and csv_tags_dict[csv_case_id][online_obj_index] != online_obj
                        ):
                            csv_tags_dict[csv_case_id][online_obj_index] = online_obj
                            flag = True
                        if (
                            skip_reason_index
                            and csv_tags_dict[csv_case_id][skip_reason_index] != skip_reason
                        ):
                            if skip_reason:
                                csv_tags_dict[csv_case_id][skip_reason_index] = skip_reason
                                flag = True

                        new_tags = csv_tags_dict[csv_case_id]
                        if flag:
                            logger.info(f"pms case id: {pms_case_id}, new tags:{new_tags}")
                        new_csv_tags.append(new_tags)
                        break
                else:
                    new_csv_tags.append(csv_tags_dict[csv_case_id])

            new_csv_file_tags[csv_path_dict.get(csv_name)] = new_csv_tags
        return new_csv_file_tags

    def write_new_csv(self):
        """写新的csv文件"""
        new_csv_file_tags = self.compare_pms_to_csv()
        for csv_file in new_csv_file_tags:
            new_csv_tags = new_csv_file_tags.get(csv_file)
            with open(csv_file, "w+", encoding="utf-8") as f:
                for tags in new_csv_tags:
                    f.write(",".join(["" if i is None else i for i in tags]) + "\n")
            logger.info(f"同步完成: {csv_file}")


if __name__ == "__main__":
    Pms2Csv().write_new_csv()
