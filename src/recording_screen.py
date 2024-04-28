#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
# pylint: disable=C0301,W0702,C0103,C0411,C0412
import time
import subprocess as sp
import os
import errno

from src.mouse_key import MouseKey
from setting.globalconfig import GlobalConfig
from src import logger
from contextlib import contextmanager


def recording_screen(name):
    """
     录制视频
    :param name: 视频名称
    :return:
    """
    record_path = (
        f'{GlobalConfig.ROOT_DIR}/report/record/{time.strftime("%Y-%m-%d", time.localtime())}/'
    )
    if not os.path.exists(record_path):
        os.makedirs(record_path)
    width, height = MouseKey.screen_size()
    cmd, paths = _create_ffmpeg_cmd(
        width,
        height,
        record_path,
        f"{time.strftime('%H时%M分%S秒', time.localtime())}_{name.encode('utf-8').decode('unicode-escape')[:40].replace('/', '_')}_autotest",
    )

    for path in paths:
        with suppress(OSError, errnos=(errno.ENOENT, errno.ENAMETOOLONG)):
            os.remove(path)
        logger.info(f"录屏路径存放  {path}")

    with open(os.devnull, "w", encoding="utf-8") as dev_null:
        with sp.Popen(cmd, stdin=sp.PIPE, stdout=dev_null, stderr=dev_null, close_fds=True) as proc:
            time.sleep(0.5)
            if proc.poll() is not None:
                raise RuntimeError("ffmpeg did not start")

            try:
                yield paths[0]
            finally:
                logger.info("停止录屏")
                try:
                    with suppress(IOError, errnos=(errno.EINVAL, errno.EPIPE)):
                        logger.debug(" stop step 1")
                        proc.communicate(input=b"q", timeout=10)
                        logger.debug(f"录屏状态 {proc.stdin.closed}")
                        if not proc.stdin.closed:
                            proc.stdin.close()
                            logger.debug("停止录屏 finish")
                except:
                    try:
                        for _ in range(5):
                            proc.communicate(input=b"q", timeout=10)
                            proc.stdin.close()
                            time.sleep(0.5)
                            if proc.stdin.closed:
                                break
                    except:
                        pass

                logger.info("停止录屏 finish")


def _create_ffmpeg_cmd(width, height, dir_path, file_name, qp=1):
    """
     组装ffmpeg命令行参数
    :param width: 宽
    :param height: 高
    :param dir_path: 视频路径
    :param file_name: 视频名称
    :param qp:
    :return:
    """
    cmd = ["ffmpeg"]

    wh = f"{width}x{height}"
    cmd.extend(
        [
            "-framerate",
            "25",
            "-video_size",
            wh,
            "-f",
            "x11grab",
            "-i",
            f"{os.environ.get('DISPLAY', None)}",
        ]
    )

    paths = []
    file_path = os.path.join(dir_path, file_name + "{}.mp4")
    output_fmt = ["-c:v", "libx264", "-qp", str(qp), "-preset", "ultrafast"]
    path = file_path.format("")
    cmd.extend(output_fmt + [path])
    paths.append(path)
    logger.debug(" ".join(cmd))
    return cmd, paths


@contextmanager
def suppress(exception, errnos):
    """
     抛异常
    :param exception:
    :param errnos:
    :return:
    """
    try:
        yield
    except exception as e:
        # logger.error(f"异常 {e}")
        if errno and e.errno not in errnos:
            logger.debug("step 2")
            raise
