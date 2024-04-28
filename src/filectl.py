#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
import os
from copy import deepcopy

from setting.globalconfig import GlobalConfig
from src import logger


class FileCtl:
    """
    Operations on system files and directories.
    Realize the addition, deletion, modification
    and query of documents.
    """

    # pylint: disable=too-many-arguments,too-many-branches,too-many-nested-blocks
    __author__ = "Mikigo <huangmingqiang@uniontech.com>, Litao <litaoa@uniontech.com>"

    @staticmethod
    def creat_files(path: str, file_name: str = "", file_type: str = "dir"):
        """
         创建文件或文件夹
        :param path: 用户下目录下的路径
        :param file_name: 文件名，默认为空
        :param file_type: 文件类型，默认 dir，文件夹， file 文件
        """
        parent_dir = f"/home/{GlobalConfig.USERNAME}/{path}"
        if file_type in ("dir", "file"):
            if file_type == "dir":
                os.system(f"mkdir -p {parent_dir}/{file_name}")
            if file_type == "file":
                if os.path.exists(parent_dir):
                    os.system(f"touch {parent_dir}/{file_name}")
                else:
                    logger.error(f"{parent_dir} is not exists!")
        else:
            logger.error(f"{file_type} is not dir or file!")

    @staticmethod
    def delete_files(path: str, ignores: tuple = (), includes: tuple = ()):
        """
         删除文件或文件夹
        :param path: 用户目录下的路径
        :param ignores: 忽略的文件列表
        :param includes: 删除的文件列表
        """
        abs_file_path = f"/home/{GlobalConfig.USERNAME}/{path}"
        if os.path.isdir(abs_file_path):
            if not isinstance(ignores, tuple):
                logger.error("ignores Parameter is not a tuple")
                raise ValueError
            if not isinstance(includes, tuple):
                logger.error("includes Parameter is not a tuple")
                raise ValueError
            file_list = os.listdir(abs_file_path)
            if file_list:
                delete_list = deepcopy(file_list)
                if ignores and not includes:
                    for file in file_list:
                        for ignore in ignores:
                            if ignore in file:
                                delete_list.remove(file)
                    if delete_list:
                        for i in delete_list:
                            os.system(
                                f"echo '{GlobalConfig.PASSWORD}' | "
                                f"sudo -S rm -rf '{abs_file_path}/{i}'"
                            )
                elif not ignores and includes:
                    for file in file_list:
                        for include in includes:
                            if include in file:
                                os.system(
                                    f"echo '{GlobalConfig.PASSWORD}' | "
                                    f"sudo -S rm -rf '{abs_file_path}/{file}'"
                                )
                elif not ignores and not includes:
                    os.system(
                        f"echo '{GlobalConfig.PASSWORD}' | " f"sudo -S rm -rf {abs_file_path}/*"
                    )
                else:
                    logger.info("This deletion mode is not supported for the time being!")
            # else:
            #     logger.info(f"There are no files in the directory <{path}!>")
        else:
            logger.error(f"{abs_file_path} is not exsits !")

    @staticmethod
    def rename_files(path: str, old_name: str, new_name: str):
        """
         重命名文件
        :param path: 用户目录下的路径
        :param old_name: 旧名字
        :param new_name: 新名字
        :return:
        """
        parent_dir = f"/home/{GlobalConfig.USERNAME}/{path}"
        old_abs_path = f"{parent_dir}/{old_name}"
        new_abs_path = f"{parent_dir}/{new_name}"
        os.system(f"mv {old_abs_path} {new_abs_path}")

    @staticmethod
    def move_files(path: str, file_name: str, new_path: str = None, new_file_name: str = None):
        """
         移动文件
        :param path: 旧路径
        :param file_name: 旧文件
        :param new_path: 新路径
        :param new_file_name: 新文件
        :return:
        """
        parent_dir = f"/home/{GlobalConfig.USERNAME}/{path}"
        new_parent_dir = f"/home/{GlobalConfig.USERNAME}/{new_path}"
        old_abs_path = f"{parent_dir}/{file_name}"
        if os.path.exists(parent_dir):
            if not new_path:
                if new_file_name:
                    new_abs_path = f"{parent_dir}/{new_file_name}"
                else:
                    new_abs_path = old_abs_path
            else:
                if new_file_name:
                    new_abs_path = f"{new_parent_dir}/{new_file_name}"
                else:
                    new_abs_path = f"{new_parent_dir}/{file_name}"
            if os.path.exists(new_parent_dir):
                os.system(f"mv {old_abs_path} {new_abs_path}")
            else:
                raise FileNotFoundError
        else:
            raise FileNotFoundError

    @classmethod
    def find_files(
        cls,
        path: str,
        startwith: str = None,
        include: str = None,
        endwith: str = None,
        not_includes: tuple = (),
        recursive: bool = False,
        abs_path: bool = False,
    ) -> list:
        """
         查找文件
        :param path: 查找路径
        :param startwith: 以 xx 开头
        :param include: 包含的文件
        :param endwith: 以 xx 结尾
        :param not_includes: 不包含的文件夹
        :param recursive: 是否查找子目录
        :param abs_path: 是否返回绝对路径列表。
        :return: 查找到的文件列表
        """
        parent_dir = f"/home/{GlobalConfig.USERNAME}/{path}"
        if os.path.exists(parent_dir):
            files_list = []
            if recursive:
                for root, _, files in os.walk(parent_dir):
                    for file in files:
                        cls.__check_not_includes(
                            not_includes,
                            endwith,
                            file,
                            files_list,
                            include,
                            startwith,
                            abs_path,
                            root,
                        )
            else:
                for file in os.listdir(parent_dir):
                    cls.__check_not_includes(
                        not_includes,
                        endwith,
                        file,
                        files_list,
                        include,
                        startwith,
                        abs_path,
                        parent_dir,
                    )
            if not files_list:
                logger.info(
                    f"查找模式：\nstartwith:{startwith}\ninclude:{include}\n"
                    f"endwith:{endwith}\nrecursive:{recursive}\n"
                    f"{parent_dir}目录下未找到该查找模式的文件～"
                )
            return files_list
        logger.error(f"{parent_dir} is not exists!")
        return []

    @classmethod
    def __check_not_includes(
        cls, not_includes, endwith, file, files_list, include, startwith, abs_path, root
    ):
        """Filter criteria for function 'find_files' parameter 'notincludes'"""
        if not_includes:
            for not_include in not_includes:
                if not_include in file:
                    continue
                cls.__check_startwith(endwith, file, files_list, include, startwith, abs_path, root)
        else:
            cls.__check_startwith(endwith, file, files_list, include, startwith, abs_path, root)

    @classmethod
    def __check_startwith(cls, endwith, file, files_list, include, startwith, abs_path, root):
        """Filter criteria for function 'find_files' parameter 'startwith'"""
        if not startwith:
            cls.__check_endwith(endwith, file, files_list, include, abs_path, root)
        else:
            if file.startswith(startwith):
                cls.__check_endwith(endwith, file, files_list, include, abs_path, root)

    @classmethod
    def __check_endwith(cls, endwith, file, files_list, include, abs_path, root):
        """Filter criteria for function 'find_files' parameter 'endwith'"""
        if not endwith:
            cls.__check_include(file, files_list, include, abs_path, root)
        else:
            if file.endswith(endwith):
                cls.__check_include(file, files_list, include, abs_path, root)

    @classmethod
    def __check_include(cls, file, files_list, include, abs_path, root):
        """Filter criteria for function 'find_files' parameter 'include'"""
        if not include:
            cls.__check_abspath(file, files_list, abs_path, root)
        else:
            if include in file:
                cls.__check_abspath(file, files_list, abs_path, root)

    @classmethod
    def __check_abspath(cls, file, files_list, abs_path, root):
        """Filter criteria for function 'find_files' parameter 'abs_path'"""
        if not abs_path:
            files_list.append(file)
        else:
            files_list.append(f"{root}/{file}")

    @staticmethod
    def file_exists(*files, abspath=False, _try=True):
        """
         查找文件，若有不存在的文件则返回None货抛出异常
        :param files: 文件列表
        :param abspath: 是否绝对路径
        :param _try: 是否抛出异常
        :return: 文件列表
        """
        if not abspath:
            abspath = f"/home/{GlobalConfig.USERNAME}"
        for file in files:
            if not os.path.exists(f"{abspath}/{file}"):
                if _try:
                    raise FileNotFoundError(file)
                return None
        return files

    @staticmethod
    def file_name_and_format(position, _format=None):
        """
         获取文件的名称和格式, 返回名称和格式组成的tuple
        :param position: 路径
        :param _format: 以 xx 结尾
        :return: 名称和格式
        """
        files = FileCtl.find_files(path=position, endwith=_format)
        for file in files:
            name_pic = file.split(".")[0]
            format_pic = file.split(".")[1]
            if "test_" in name_pic:
                return name_pic, format_pic
            return None, None
        return None, None


if __name__ == "__main__":
    FileCtl.delete_files("Desktop", includes=("新建",))
