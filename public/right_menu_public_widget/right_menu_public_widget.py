#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
import letmego

from src.image_utils import ImageUtils
from src import sleep, log
from src import logger
from src import ShortCut
from public.right_menu_public_widget.config import Config

@letmego.mark
@log
# pylint: disable=too-many-public-methods
class RightMenuPublicWidget(ImageUtils, ShortCut):
    """右键菜单选项
    通过图像识别操作右键菜单
    """

    @classmethod
    def click_right_menu_by_image(cls, pic):
        """
         点击右键菜单中的相应选项
        :param pic: 图片路径
        """
        cls.click(*cls.find_image(f"{Config.PIC_RES_PATH}/{pic}"))

    @classmethod
    def click_always_at_the_top_in_right_menu_by_image(cls):
        """
         点击“总在最前”
        :return:
        """
        cls.click_right_menu_by_image("always_at_the_top")
        logger.info("点击“总在最前”")

    @classmethod
    def click_close_window_in_right_menu_by_image(cls):
        """
         点击“关闭”
        :return:
        """
        cls.click_right_menu_by_image("close")
        logger.info("点击“关闭”")

    @classmethod
    def click_reduction_in_right_menu_by_image(cls):
        """
         点击“还原”
        :return:
        """
        cls.click_right_menu_by_image("reduction")
        logger.info("点击“还原”")

    @classmethod
    def click_minimize_in_right_menu_by_image(cls):
        """
         点击“最小化”
        :return:
        """
        cls.click_right_menu_by_image("minimize")
        logger.info("点击“最小化”")

    @classmethod
    def click_change_size_in_right_menu_by_image(cls):
        """
         点击“更改大小”
        :return:
        """
        cls.click_right_menu_by_image("change_size")
        logger.info("点击“更改大小”")

    @classmethod
    def click_move_in_right_menu_by_image(cls):
        """
         点击“移动”
        :return:
        """
        cls.click_right_menu_by_image("move")
        logger.info("点击“移动”")

    @classmethod
    def click_maximize_in_right_menu_by_image(cls):
        """
         点击“最大化”
        :return:
        """
        cls.click_right_menu_by_image("maximize")
        logger.info("点击“最大化”")

    @classmethod
    def click_always_in_the_visible_workspace_in_right_menu_by_image(cls):
        """
         点击“总在可见工作区”
        :return:
        """
        cls.click_right_menu_by_image("always_in_the_visible_workspace")
        logger.info("点击“总在可见工作区”")

    @classmethod
    def click_move_to_left_workspace_in_right_menu_by_image(cls):
        """
         点击“移至左边工作区“
        :return:
        """
        cls.click_right_menu_by_image("move_to_left_workspace")
        logger.info("点击“移至左边工作区”")

    @classmethod
    def click_move_to_right_workspace_in_right_menu_by_image(cls):
        """
         点击“移至右边工作区“
        :return:
        """
        cls.click_right_menu_by_image("move_to_right_workspace")
        logger.info("点击“移至右边工作区”")

    @classmethod
    def click_open_in_right_menu_by_image(cls):
        """
         点击“打开”
        :return:
        """
        cls.click_right_menu_by_image("open")
        logger.info("点击“打开”")

    @classmethod
    def click_open_mode_in_right_menu_by_image(cls):
        """
         点击“打开方式”
        :return:
        """
        cls.click_right_menu_by_image("open_mode")
        logger.info("点击“打开方式”")

    @classmethod
    def click_attribute_in_right_menu_by_image(cls):
        """
         点击“属性”
        :return:
        """
        cls.click_right_menu_by_image("attribute")
        sleep(1)
        logger.info("点击“属性”")

    @classmethod
    def click_share_manager_in_right_menu_by_image(cls):
        """
         点击“共享管理”
        :return:
        """
        cls.click_right_menu_by_image("share_manager")
        sleep(1)
        logger.info("点击“共享管理”")

    @classmethod
    def click_defender_in_right_menu_by_image(cls):
        """
         点击“病毒查杀”
        :return:
        """
        cls.click_right_menu_by_image("defender")
        logger.info("点击“病毒查杀”")

    @classmethod
    def click_cd_burn_in_right_menu_by_image(cls):
        """
         点击“光盘刻录”
        :return:
        """
        cls.click_right_menu_by_image("CD_burn")
        logger.info("点击“光盘刻录”")

    @classmethod
    def click_compress_in_right_menu_by_image(cls):
        """
         点击“压缩”
        :return:
        """
        cls.click_right_menu_by_image("compress")
        logger.info("点击“压缩”")

    @classmethod
    def click_copy_in_right_menu_by_image(cls):
        """
         点击“复制”
        :return:
        """
        cls.click_right_menu_by_image("copy")
        logger.info("点击“复制”")

    @classmethod
    def click_uncompress_in_right_menu_by_image(cls):
        """
         点击“解压”
        :return:
        """
        cls.click_right_menu_by_image("uncompress")
        logger.info("点击“解压”")

    @classmethod
    def click_paste_in_right_menu_by_image(cls):
        """
         点击“粘贴”
        :return:
        """
        cls.click_right_menu_by_image("paste")
        logger.info("点击“粘贴”")

    @classmethod
    def click_cut_in_right_menu_by_image(cls):
        """
         点击“剪切”
        :return:
        """
        cls.click_right_menu_by_image("cut")
        logger.info("点击“剪切”")

    @classmethod
    def click_delete_in_right_menu_by_image(cls):
        """
         点击“删除”
        :return:
        """
        cls.click_right_menu_by_image("delete")
        logger.info("点击“删除”")

    @classmethod
    def click_create_link_in_right_menu_by_image(cls):
        """
         点击“创建链接”
        :return:
        """
        cls.click_right_menu_by_image("link")
        logger.info("点击“创建链接”")

    @classmethod
    def click_mark_information_in_right_menu_by_image(cls):
        """
         点击“标记信息”
        :return:
        """
        cls.click_right_menu_by_image("mark_information")
        logger.info("点击“标记信息”")

    @classmethod
    def click_new_label_in_right_menu_by_image(cls):
        """
         点击“在新标签中打开”
        :return:
        """
        cls.click_right_menu_by_image("new_label")
        logger.info("点击“在新标签中打开”")

    @classmethod
    def click_copy_path_right_menu_by_image(cls):
        """
         点击“复制路径”
        :return:
        """
        cls.click_right_menu_by_image("copy_path")
        logger.info("点击“复制路径”")

    @classmethod
    def click_edit_path_right_menu_by_image(cls):
        """
         点击“编辑路径”
        :return:
        """
        cls.click_right_menu_by_image("edit_path")
        logger.info("点击“编辑路径”")

    @classmethod
    def click_new_window_in_right_menu_by_image(cls):
        """
         点击“新窗口”
        :return:
        """
        cls.click_right_menu_by_image("new_window")
        logger.info("点击“新窗口”")

    @classmethod
    def click_rename_in_right_menu_by_image(cls):
        """
         点击“重命名”
        :return:
        """
        cls.click_right_menu_by_image("rename")
        logger.info("点击“重命名”")

    @classmethod
    def click_send_to_in_right_menu_by_image(cls):
        """
         点击“发送到”
        :return:
        """
        cls.click_right_menu_by_image("send_to")
        logger.info("点击“发送到”")

    @classmethod
    def click_send_to_uos_in_right_menu_by_image(cls):
        """
         点击“发送到-UOS”
        :return:
        """
        cls.click_right_menu_by_image("UOS")
        logger.info("点击“发送到-UOS”")

    @classmethod
    def click_send_to_desktop_in_right_menu_by_image(cls):
        """
         点击“发送到桌面”
        :return:
        """
        cls.click_right_menu_by_image("send_to_desktop")
        logger.info("点击“发送到桌面”")

    @classmethod
    def click_share_folder_in_right_menu_by_image(cls):
        """
         点击“共享文件夹”
        :return:
        """
        cls.click_right_menu_by_image("share_folder")
        sleep(1)
        logger.info("点击“共享文件夹”")

    @classmethod
    def click_cancel_share_folder_in_right_menu_by_image(cls):
        """
         点击“取消共享文件夹”
        :return:
        """
        cls.click_right_menu_by_image("cancel_share")
        logger.info("点击“取消共享文件夹”")

    @classmethod
    def click_terminal_in_right_menu_by_image(cls):
        """
         点击“终端打开”
        :return:
        """
        cls.click_right_menu_by_image("terminal")
        logger.info("点击“终端打开”")

    @classmethod
    def click_editor_in_right_menu_by_image(cls):
        """
         点击“文本编辑器”
        :return:
        """
        cls.click_right_menu_by_image("editor")
        logger.info("点击“文本编辑器”")

    @classmethod
    def click_file_manager_in_right_menu_by_image(cls):
        """
         点击“文件管理器“
        :return:
        """
        cls.click_right_menu_by_image("file_manager")
        logger.info("点击“文件管理器“")

    @classmethod
    def click_ok_in_right_menu_by_image(cls):
        """
         点击“确定”
        :return:
        """
        cls.click_right_menu_by_image("ok")
        logger.info("点击“确定”")

    @classmethod
    def click_add_bookmark_in_right_menu_by_image(cls):
        """
         点击“添加书签”
        :return:
        """
        cls.click_right_menu_by_image("bookmark")
        logger.info("点击“添加书签”")

    @classmethod
    def click_remove_bookmark_in_right_menu_by_image(cls):
        """
         点击“移除书签”
        :return:
        """
        cls.click_right_menu_by_image("remove_bookmark")
        logger.info("点击“移除书签”")

    @classmethod
    def click_select_default_app_in_right_menu_by_image(cls):
        """
         点击“选择默认程序”
        :return:
        """
        cls.click_right_menu_by_image("select_default_app")
        logger.info("点击“选择默认程序”")

    @classmethod
    def click_open_file_path_in_right_menu_by_image(cls):
        """
         点击“选择打开文件位置”
        :return:
        """
        cls.click_right_menu_by_image("open_file_path")
        logger.info("点击“选择打开文件位置”")

    @classmethod
    def click_open_with_edit_in_right_menu_by_image(cls):
        """
         点击“选择文件编辑器打开”
        :return:
        """
        cls.click_right_menu_by_image("deepin-editor")
        logger.info("点击“选择文件编辑器打开”")

    @classmethod
    def click_remove_in_right_menu_by_image(cls):
        """
         点击“选择移除”
        :return:
        """
        cls.click_right_menu_by_image("remove")
        logger.info("点击“选择移除”")

    @classmethod
    def click_recycle_all_in_right_menu_by_image(cls):
        """
         点击“全部还原”
        :return:
        """
        cls.click_right_menu_by_image("recycle_all")
        logger.info("点击“全部还原”")

    @classmethod
    def click_empty_trash_in_right_menu_by_image(cls):
        """
         点击“清空回收站”
        :return:
        """
        cls.click_right_menu_by_image("empty_trash")
        logger.info("点击“清空回收站”")

    @classmethod
    def click_show_mode_in_right_menu_by_image(cls):
        """
         点击“选择显示方式”
        :return:
        """
        cls.click_right_menu_by_image("show_mode")
        logger.info("点击“选择显示方式”")

    @classmethod
    def click_icon_mode_in_right_menu_by_image(cls):
        """
         点击“选择图标方式”
        :return:
        """
        cls.click_right_menu_by_image("icon_mode")
        logger.info("点击“选择图标方式”")

    @classmethod
    def click_list_mode_in_right_menu_by_image(cls):
        """
         点击“选择列表方式”
        :return:
        """
        cls.click_right_menu_by_image("list_mode")
        logger.info("点击“选择列表方式”")

    @classmethod
    def click_recycle_in_right_menu_by_image(cls):
        """
         点击“选择还原”
        :return:
        """
        cls.click_right_menu_by_image("recycle")
        logger.info("点击“选择还原”")

    @classmethod
    def click_delete_vault_in_right_menu_by_image(cls):
        """
         点击“删除保险箱”
        :return:
        """
        cls.click_right_menu_by_image("delete_vault")
        logger.info("点击“删除保险箱”")

    @classmethod
    def click_lock_now_in_right_menu_by_image(cls):
        """
         点击“立即上锁”
        :return:
        """
        cls.click_right_menu_by_image("lock_now")
        logger.info("点击“立即上锁”")

    @classmethod
    def click_key_unlock_in_right_menu_by_image(cls):
        """
         点击“密钥解锁”
        :return:
        """
        cls.click_right_menu_by_image("key_unlock")
        logger.info("点击“密钥解锁”")

    @classmethod
    def click_set_wallpaper_in_right_menu_by_image(cls):
        """
         点击“设置壁纸”
        :return:
        """
        cls.click_right_menu_by_image("set_wallpaper")
        logger.info("点击“设置壁纸”")

    @classmethod
    def click_open_with_root_in_right_menu_by_image(cls):
        """
         点击“以管理打开”
        :return:
        """
        cls.click_right_menu_by_image("open_with_root")
        logger.info("点击“以管理打开”")

    @classmethod
    def click_new_folder_in_right_menu_by_image(cls):
        """
         点击“新建文件夹”
        :return:
        """
        cls.click_right_menu_by_image("new_folder")
        logger.info("点击“新建文件夹”")

    @classmethod
    def click_auto_sort_in_right_menu_by_image(cls):
        """
         点击“自动排序”
        :return:
        """
        cls.click_right_menu_by_image("auto_sort")
        logger.info("点击“自动排序”")

    @classmethod
    def click_display_setting_in_right_menu_by_image(cls):
        """
         点击“显示设置”
        :return:
        """
        cls.click_right_menu_by_image("display_setting")
        logger.info("点击“显示设置”")

    @classmethod
    def click_excel_in_right_menu_by_image(cls):
        """
         点击“表格”
        :return:
        """
        cls.click_right_menu_by_image("excel")
        logger.info("点击“表格”")

    @classmethod
    def click_icon_size_in_right_menu_by_image(cls):
        """
         点击“图标大小”
        :return:
        """
        cls.click_right_menu_by_image("icon_size")
        logger.info("点击“图标大小”")

    @classmethod
    def click_minist_in_right_menu_by_image(cls):
        """
         点击“极小”
        :return:
        """
        cls.enter()
        cls.select_submenu(1)
        logger.info("点击“极小”")

    @classmethod
    def click_mini_in_right_menu_by_image(cls):
        """
         点击“小”
        :return:
        """
        # cls.click_image("mini")
        cls.enter()
        cls.select_submenu(2)
        logger.info("点击“小”")

    @classmethod
    def click_middle_in_right_menu_by_image(cls):
        """
         点击“中”
        :return:
        """
        # cls.click_image("middle")
        cls.enter()
        cls.select_submenu(3)
        logger.info("点击“中”")

    @classmethod
    def click_big_in_right_menu_by_image(cls):
        """
         点击“大”
        :return:
        """
        # cls.click_image("big")
        cls.enter()
        cls.select_submenu(4)
        logger.info("点击“大”")

    @classmethod
    def click_bigist_in_right_menu_by_image(cls):
        """
         点击“极大”
        :return:
        """
        cls.click_right_menu_by_image("bigist")
        logger.info("点击“极大”")

    @classmethod
    def click_name_in_right_menu_by_image(cls):
        """
         点击“名称”
        :return:
        """
        cls.click_right_menu_by_image("name")
        logger.info("点击“名称”")

    @classmethod
    def click_path_in_right_menu_by_image(cls):
        """
         点击“路径”
        :return:
        """
        cls.click_right_menu_by_image("path")
        logger.info("点击“路径”")

    @classmethod
    def click_latest_visit_time_in_right_menu_by_image(cls):
        """
         点击“最近访问时间”
        :return:
        """
        cls.click_right_menu_by_image("latest_visit_time")
        logger.info("点击“最近访问时间”")

    @classmethod
    def click_new_document_in_right_menu_by_image(cls):
        """
         点击“新建文档”
        :return:
        """
        cls.click_right_menu_by_image("new_document")
        sleep(1)
        logger.info("点击“新建文档”")

    @classmethod
    def click_ppt_in_right_menu_by_image(cls):
        """
         点击“ppt”
        :return:
        """
        cls.click_right_menu_by_image("ppt")
        logger.info("点击“ppt”")

    @classmethod
    def click_select_all_in_right_menu_by_image(cls):
        """
         点击“全选”
        :return:
        """
        cls.click_right_menu_by_image("select_all")
        logger.info("点击“全选”")

    @classmethod
    def click_size_in_right_menu_by_image(cls):
        """
         点击“大小”
        :return:
        """
        cls.click_right_menu_by_image("size")
        logger.info("点击“大小”")

    @classmethod
    def click_word_size_in_right_menu_by_image(cls):
        """
         点击“文件大小”
        :return:
        """
        cls.click_right_menu_by_image("word_size")
        logger.info("点击“文件大小”")

    @classmethod
    def click_word_type_in_right_menu_by_image(cls):
        """
         点击“类型”
        :return:
        """
        cls.click_right_menu_by_image("word_type")
        logger.info("点击“类型”")

    @classmethod
    def click_original_path_in_right_menu_by_image(cls):
        """
         点击“原始路径”
        :return:
        """
        cls.click_right_menu_by_image("original_path")
        logger.info("点击“原始路径”")

    @classmethod
    def click_delete_time_in_right_menu_by_image(cls):
        """
         点击“删除时间”
        :return:
        """
        cls.click_right_menu_by_image("delete_time")
        sleep(1)
        logger.info("点击“删除时间”")

    @classmethod
    def click_sort_method_in_right_menu_by_image(cls):
        """
         点击“排序方法”
        :return:
        """
        cls.click_right_menu_by_image("sort_method")
        sleep(1)
        logger.info("点击“排序方法”")

    @classmethod
    def click_change_time_in_right_menu_by_image(cls):
        """
         点击“修改时间”
        :return:
        """
        cls.click_right_menu_by_image("time")
        logger.info("点击“修改时间”")

    @classmethod
    def click_txt_in_right_menu_by_image(cls):
        """
         点击“txt”
        :return:
        """
        cls.click_right_menu_by_image("txt")
        logger.info("点击“txt”")

    @classmethod
    def click_type_in_right_menu_by_image(cls):
        """
         点击“类型”
        :return:
        """
        cls.click_right_menu_by_image("type")
        logger.info("点击“类型”")

    @classmethod
    def click_wallpaper_in_right_menu_by_image(cls):
        """
         点击“壁纸”
        :return:
        """
        cls.click_right_menu_by_image("wallpaper")
        logger.info("点击“壁纸”")

    @classmethod
    def click_word_in_right_menu_by_image(cls):
        """
         点击“word”
        :return:
        """
        cls.click_right_menu_by_image("word")
        logger.info("点击“word”")

    @classmethod
    def click_default_application_by_image(cls):
        """
         点击“选择默认程序”
        :return:
        """
        cls.click_right_menu_by_image("default_application")
        sleep(1)
        logger.info("点击“选择默认程序”")

    @classmethod
    def click_add_dir_to_zip_by_image(cls):
        """
         点击 ”添加到新建文件夹.zip”
        :return:
        """
        cls.click_right_menu_by_image("add_to_zip")
        logger.info("点击 添加到新建文件夹.zip")

    @classmethod
    def click_add_desktop_zip_by_image(cls):
        """
         点击 “添加到Desktop.zip”
        :return:
        """
        cls.click_right_menu_by_image("add_desktop_zip")
        logger.info("点击 添加到Desktop.zip")

    @classmethod
    def click_list_view_in_right_menu_by_image(cls):
        """
         点击“列表视图“
        :return:
        """
        cls.click_right_menu_by_image("list_view")
        logger.info("点击“列表视图”")

    @classmethod
    def click_icon_view_in_right_menu_by_image(cls):
        """
         点击“图标视图”
        :return:
        """
        cls.click_right_menu_by_image("icon_view")
        logger.info("点击“图标视图”")

    @classmethod
    def click_noanonymity_in_right_menu_by_image(cls):
        """
         点击不允许下拉框
        :return:
        """
        cls.click_right_menu_by_image("no_anonymity")
        logger.info("点击不允许下拉框")

    @classmethod
    def click_anonymity_in_right_menu_by_image(cls):
        """
         点击下拉框的允许选项
        :return:
        """
        cls.click_right_menu_by_image("anonymity")
        logger.info("点击下拉框的允许选项")
