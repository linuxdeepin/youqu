import getpass
import os
import pathlib
import platform
import time


class ArchName:
    x86 = "x86_64"
    aarch64 = "aarch64"
    loongarch64 = "loongarch64"
    mips64 = "mips64"
    sw64 = "sw64"


class DisplayServer:
    wayland = "wayland"
    x11 = "x11"


class _DynamicSetting:
    SYS_ARCH = platform.machine().lower()
    HOME = str(pathlib.Path.home())
    USERNAME = getpass.getuser()

    YOUQU_HOME = pathlib.Path(__file__).parent.parent
    TPL_PATH = YOUQU_HOME / "tpl"
    RPC_PATH = YOUQU_HOME / "gui" / "_rpc"

    if os.path.exists(os.path.expanduser("~/.xsession-errors")):
        DISPLAY_SERVER = (
            os.popen("cat ~/.xsession-errors | grep XDG_SESSION_TYPE | head -n 1")
            .read()
            .split("=")[-1]
            .strip("\n")
        )
    else:
        DISPLAY_SERVER = "x11" if os.popen("ps -ef | grep -v grep | grep kwin_x11").read() else "wayland"

    IS_X11: bool = DISPLAY_SERVER == DisplayServer.x11
    IS_WAYLAND: bool = DISPLAY_SERVER == DisplayServer.wayland

    TIME_STRING = time.strftime("%Y%m%d%H%M%S")
    HOST_IP = str(os.popen("hostname -I |awk '{print $1}'").read()).strip("\n").strip()
