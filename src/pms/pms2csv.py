#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
# pylint: disable=C0301,C0115,R0903,C0103,C0201,R1710,R0914,W1514,R0914,R1702
import json
import os
import re
from configparser import ConfigParser
from os.path import splitext
from time import strftime
from pprint import pprint

from setting.globalconfig import GetCfg
from setting.globalconfig import GlobalConfig
from src  import logger
from src.pms._base import MAX_CASE_NUMBER
from src.pms._base import _Base
from src.pms._base import _unicode_to_cn


class CsvTitle:
    case_id = "PMS用例ID"
    case_level = "用例级别"


class Pms2Csv(_Base):
    """爬取pms数据同步到本地csv文件"""

    __author__ = "huangmingqiang@uniontech.com"

    def __init__(self):
        super().__init__()
        self.APP_NAME = GlobalConfig.APP_NAME
        self.project_dir = f"autotest_{self.APP_NAME.replace('-', '_')}"
        if not os.path.exists(f"{GlobalConfig.APPS_PATH}/{self.project_dir}"):
            logger.error(f"{self.project_dir} 似乎不存在 !")
            raise ValueError

        self.PMS_USER = GlobalConfig.PMS_USER
        self.PMS_PASSWORD = GlobalConfig.PMS_PASSWORD

        conf = ConfigParser()
        conf.read(GlobalConfig.GLOBAL_CONFIG_FILE_PATH)
        self.csv_names = conf.options("csv_link_pms_id")
        self.csv_link_cfg = GetCfg(
            GlobalConfig.GLOBAL_CONFIG_FILE_PATH, "csv_link_pms_id"
        )
        csv_link_lib_cfg = GetCfg(
            GlobalConfig.GLOBAL_CONFIG_FILE_PATH, "csv_link_pms_lib"
        )
        self.CASE_FROM = csv_link_lib_cfg.get("CASE_FROM", default="caselib")

    def get_data(self, app_case_id):
        """获取pms上数据"""
        case_url = (
            f"https://pms.uniontech.com/{self.CASE_FROM}-browse-"
            f'{app_case_id}-{"-" if self.CASE_FROM == "testcase" else ""}all-0-id_desc-0-{MAX_CASE_NUMBER}.json'
        )
        res = self.rx.open_url(case_url)
        res_str = _unicode_to_cn(res)

        try:
            res_dict = json.loads(res_str)
        except json.decoder.JSONDecodeError:
            logger.error(f"爬取pms数据失败, 请检查模块 id 是否为: {app_case_id}")
            return

        cases = res_dict.get("data").get("cases")
        res_data = {}
        for i in cases:
            case_id = cases.get(i).get("id")
            case_level = cases.get(i).get("pri")
            case_title = cases.get(i).get("title")
            # 从用例标题中取出自动化用例id [001]
            at_case_id = re.findall(r"\[(\d{3})\]", case_title)
            # 如果id存在，并且之前没有出现过
            # 如果出现相同的id，只取第一个
            if at_case_id and at_case_id[0] not in res_data.keys():
                # 组装成一个字典
                res_data[at_case_id[0]] = {
                    "case_id": case_id,  # 用例在PMS上ID
                    "case_level": case_level,  # 用例级别
                    "case_title": case_title,  # 用例标题
                }
        if not res_data:
            logger.error("未从pms获取到数据, 请检查配置")
            raise ValueError
        return res_data

    def read_csv(self):
        """读取本地csv文件数据"""
        csv_path_dict = {}
        # 默认的csv文件备份路径
        csv_bak_path = f"{GlobalConfig.REPORT_PATH}/csv_back"
        if not os.path.exists(csv_bak_path):
            os.makedirs(csv_bak_path)
        for root, _, files in os.walk(f"{GlobalConfig.APPS_PATH}/{self.project_dir}"):
            for file in files:
                # 必须是标签csv文件，排除一些ddt的csv文件
                if file.endswith(".csv") and splitext(file)[0] in self.csv_names:
                    csv_path_dict[splitext(file)[0]] = f"{root}/{file}"
                    # 备份csv文件
                    os.system(
                        f"cp {root}/{file} {csv_bak_path}/{strftime('%Y%m%d%H%M%S')}_{file}"
                    )
        if not csv_path_dict:
            logger.error(f"{self.APP_NAME} 目录下未找到csv文件")
            raise ValueError

        pms_id_index = None
        level_index = None
        res_tags = {}
        csv_title_dict = {}
        for csv_name in csv_path_dict:
            with open(csv_path_dict.get(csv_name), "r") as f:
                txt_list = f.readlines()
            csv_titles = txt_list[0].strip().split(",")
            for index, title in enumerate(csv_titles):
                # 找到在表头中对应的索引
                if title.strip() == CsvTitle.case_id:
                    pms_id_index = index - 1
                elif title.strip() == CsvTitle.case_level:
                    level_index = index - 1

            # 读取到所有的标签
            taglines = [txt.strip().split(",") for txt in txt_list[1:]]
            id_tags_dict = {f"{int(i[0]):0>3}": i[1:] for i in taglines if i[0]}
            res_tags[csv_name] = id_tags_dict
            # csv文件的表头
            csv_title_dict[csv_name] = csv_titles
        # 将这些数据无情的返回, 其实可以进一步将这些返回数据整合一下, 但是累了, 就这样吧
        return pms_id_index, level_index, res_tags, csv_path_dict, csv_title_dict

    def compare_pms_to_csv(self):
        """对比pms上数据和本地csv文件数据"""
        # 接收csv文件里面的值
        (
            pms_id_index,
            level_index,
            _res_tags,
            csv_path_dict,
            csv_title_dict,
        ) = self.read_csv()
        # 将csv文件里面的数据和pms上爬取的数据进行对比
        new_csv_tags_map = {}
        for csv_name in _res_tags:
            # 每个csv文件处理一次
            pms_tags_dict = self.get_data(self.csv_link_cfg.get(csv_name))
            # 如果pms上没有爬取到，继续处理下一个csv文件
            if pms_tags_dict is None:
                continue
            csv_tags_dict = _res_tags.get(csv_name)
            new_csv_tags = {}
            for csv_tag_id in csv_tags_dict:
                csv_tags = csv_tags_dict.get(csv_tag_id)
                # 拿着csv里面的id去和pms上的id匹配
                for pms_tag_id in pms_tags_dict:
                    if pms_tag_id == csv_tag_id:
                        pms_tags = pms_tags_dict.get(pms_tag_id)
                        case_id = pms_tags.get("case_id")
                        case_level = pms_tags.get("case_level")
                        case_level = f"L{case_level}"
                        # 循环处理每个字段
                        for target_index, value, title_name in [
                            [pms_id_index, case_id, CsvTitle.case_id],
                            [level_index, case_level, CsvTitle.case_level],
                        ]:
                            # 如果没有索引，说明原来csv文件中没有这一列，直接添加到最后一列
                            if target_index is None:
                                csv_tags.append(value)
                                if CsvTitle.case_id not in csv_title_dict.get(csv_name):
                                    csv_title_dict[csv_name].append(title_name)
                            else:
                                # 如果有索引，直接修改原来的数据
                                csv_tags[target_index] = value
                        break
                else:
                    # 如果此AT id没有找到对应的，那需要将csv此行补位空字符串
                    for target_index in [pms_id_index, level_index]:
                        # 如果没有索引，说明原来csv文件中没有这一列，
                        # 添加一个空字符串到最后一列
                        if target_index is None:
                            csv_tags.append("")
                new_csv_tags[csv_tag_id] = csv_tags
            new_csv_tags_map[csv_name] = new_csv_tags

        return new_csv_tags_map, csv_path_dict, csv_title_dict

    def write_new_csv(self):
        """写新的csv文件"""
        new_csv_tags_map, csv_path_dict, csv_title_dict = self.compare_pms_to_csv()
        # 将 new_csv_tags_map 里面的数据写成一个新的csv文件
        for csv_name in new_csv_tags_map:
            csv_path = csv_path_dict.get(csv_name)
            new_csv_tags = new_csv_tags_map.get(csv_name)
            new_csv_tags_list = []
            # 先把表头放进去
            new_csv_tags_list.append(",".join(csv_title_dict.get(csv_name)) + "\n")
            # 组装成一行行的数据
            for _id in new_csv_tags:
                new_csv_list = new_csv_tags.get(_id)
                new_csv_list.insert(0, _id)
                new_csv_tags_list.append(",".join(new_csv_list) + "\n")
            with open(csv_path, "w+", encoding="utf-8") as f:
                f.writelines(new_csv_tags_list)
            pprint(new_csv_tags_list, indent=4)
        logger.info("同步完成")


if __name__ == "__main__":
    Pms2Csv().write_new_csv()
