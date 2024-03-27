# -*- coding: utf-8 -*-
# This file was modified by UnionTech Software Technology Co., Ltd. in 2022/08/11
# pylint: disable=C0301,W0511,C0103,C0116,W0107,R1705,W0613,R0913,W0612,W0703,C0201,C0121,C0114,W0603,C0123
__author__ = "zhaoyouzhi@uniontech.com"
__contributor__ = "huangmingqiang@uniontech.com"

import os
import sys
from functools import wraps
from time import sleep

# from PIL import Image

from src.cmdctl import CmdCtl

if sys.version_info[0] == 2 or sys.version_info[0:2] in ((3, 1), (3, 7)):
    # Python 2 and 3.1 and 3.2 uses collections.Sequence
    import collections

# In seconds. Any duration less than this is rounded to 0.0 to instantly move
# the mouse.
MINIMUM_DURATION = 0.1
# If sleep_amount is less than MINIMUM_DURATION, sleep() will be a no-op and the mouse cursor moves there instantly.
# TODO: This value should vary with the platform. http://stackoverflow.com/q/1133857
MINIMUM_SLEEP = 0.05
STEP_SLEEP = 10

# The number of seconds to pause after EVERY public function call. Useful for debugging:
PAUSE = 0.1  # Tenth-second pause by default.

FAILSAFE = True

Point = collections.namedtuple("Point", "x y")
Size = collections.namedtuple("Size", "width height")

bshift = False

LEFT = "left"
MIDDLE = "middle"
RIGHT = "right"
PRIMARY = "left"
SECONDARY = "secondary"

dbus_cmd = "dbus-send --session --dest=com.deepin.Autotool --print-reply  /com/deepin/Autotool com.deepin.Autotool"

def context_manager(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tool_status = os.popen("ps -aux |  grep wayland_autotool | grep -v grep").read()
        if not tool_status:
            os.environ["QT_WAYLAND_SHELL_INTEGRATION"] = "kwayland-shell"
            os.environ["XDG_SESSION_DESKTOP"] = "Wayland"
            os.environ["XDG_SESSION_TYPE"] = "wayland"
            os.environ["WAYLAND_DISPLAY"] = "wayland-0"
            os.environ["GDMSESSION"] = "Wayland"
            os.environ["DBUS_SESSION_BUS_ADDRESS"] = "unix:path=/run/user/1000/bus"
            res = os.popen("nohup wayland_autotool > result.log 2>&1 &").read()
            if "未找到命令" in res:
                raise EnvironmentError("wayland_autotool没有安装")
            sleep(2)

        return func(*args, **kwargs)

    return wrapper


@context_manager
def system(cmd):
    CmdCtl.run_cmd(cmd, out_debug_flag=False, command_log=False)


@context_manager
def popen(cmd):
    return CmdCtl.run_cmd(cmd, out_debug_flag=False, command_log=False)


KEY_NAMES = {
    ' ': 57,
    '\'': 40,
    '*': 55,
    '+': 78,
    ',': 51,
    '-': 12,
    '.': 52,
    '/': 53,
    '0': 11,
    '1': 2,
    '2': 3,
    '4': 5,
    '5': 6,
    '3': 4,
    '6': 7,
    '7': 8,
    '8': 9,
    '9': 10,
    ';': 39,
    '=': 13,
    '[': 26,
    '\\': 43,
    ']': 27,
    '`': 41,
    'a': 30,
    'b': 48,
    'c': 46,
    'd': 32,
    'e': 18,
    'f': 33,
    'g': 34,
    'h': 35,
    'i': 23,
    'j': 36,
    'k': 37,
    'l': 38,
    'm': 50,
    'n': 49,
    'o': 24,
    'p': 25,
    'q': 16,
    'r': 19,
    's': 31,
    't': 20,
    'u': 22,
    'v': 47,
    'w': 17,
    'x': 45,
    'y': 21,
    'z': 44,
    'add': 78,
    'alt': 56,
    'altleft': 56,
    'altright': 100,
    'backspace': 14,
    'capslock': 58,
    'ctrl': 29,
    'ctrlleft': 29,
    'ctrlright': 97,
    'del': 111,
    'delete': 111,
    'down': 108,
    'end': 107,
    'enter': 28,
    'esc': 1,
    'escape': 1,
    'f1': 59,
    'f10': 68,
    'f11': 87,
    'f12': 88,
    'f13': 183,
    'f14': 184,
    'f15': 185,
    'f16': 186,
    'f17': 187,
    'f18': 188,
    'f19': 189,
    'f2': 60,
    'f20': 190,
    'f21': 191,
    'f22': 192,
    'f23': 193,
    'f24': 194,
    'f3': 61,
    'f4': 62,
    'f5': 63,
    'f6': 64,
    'f7': 65,
    'f8': 66,
    'f9': 67,
    'home': 172,
    'insert': 110,
    'left': 105,
    'num0': 82,
    'num1': 79,
    'num2': 80,
    'num3': 81,
    'num4': 75,
    'num5': 76,
    'num6': 77,
    'num7': 71,
    'num8': 72,
    'num9': 73,
    'numlock': 69,
    'pagedown': 109,
    'pageup': 104,
    'pgdn': 109,
    'pgup': 104,
    'print': 210,
    'right': 106,
    'scrolllock': 70,
    'shift': 42,
    'shiftleft': 42,
    'shiftright': 54,
    'space': 57,
    'tab': 15,
    'up': 103,
    'volumedown': 114,
    'volumeup': 115,
    'win': 125,
    'winleft': 125,
    'winright': 126,
    ")": 11,
    "!": 2,
    "@": 3,
    "#": 4,
    "$": 5,
    "%": 6,
    "^": 7,
    "&": 8,
    "(": 10,
    "_": 12,
    "~": 41,
    "{": 26,
    "}": 27,
    "|": 43,
    ":": 39,
    "\"": 40,
    "<": 51,
    ">": 52,
    "?": 53,
    'A': 30,
    'B': 48,
    'C': 46,
    'D': 32,
    'E': 18,
    'F': 33,
    'G': 34,
    'H': 35,
    'I': 23,
    'J': 36,
    'K': 37,
    'L': 38,
    'M': 50,
    'N': 49,
    'O': 24,
    'P': 25,
    'Q': 16,
    'R': 19,
    'S': 31,
    'T': 20,
    'U': 22,
    'V': 47,
    'W': 17,
    'X': 45,
    'Y': 21,
    'Z': 44,
    '。': 52
}

KEY_NAMES_S = {
    ")": 11,
    "!": 2,
    "@": 3,
    "#": 4,
    "$": 5,
    "%": 6,
    "^": 7,
    "&": 8,
    "(": 10,
    "_": 12,
    "~": 41,
    "{": 26,
    "}": 27,
    "|": 43,
    ":": 39,
    "\"": 40,
    "<": 51,
    ">": 52,
    "?": 53,
    'A': 30,
    'B': 48,
    'C': 46,
    'D': 32,
    'E': 18,
    'F': 33,
    'G': 34,
    'H': 35,
    'I': 23,
    'J': 36,
    'K': 37,
    'L': 38,
    'M': 50,
    'N': 49,
    'O': 24,
    'P': 25,
    'Q': 16,
    'R': 19,
    'S': 31,
    'T': 20,
    'U': 22,
    'V': 47,
    'W': 17,
    'X': 45,
    'Y': 21,
    'Z': 44
}


class PyAutoGUIException(Exception):
    """
    PyAutoGUI code will raise this exception class for any invalid actions. If PyAutoGUI raises some other exception,
    you should assume that this is caused by a bug in PyAutoGUI itself. (Including a failure to catch potential
    exceptions raised by PyAutoGUI.)
    """
    pass


def getPointOnLine(x1, y1, x2, y2, n):
    """
    Returns an (x, y) tuple of the point that has progressed a proportion ``n`` along the line defined by the two
    ``x1``, ``y1`` and ``x2``, ``y2`` coordinates.

    This function was copied from pytweening module, so that it can be called even if PyTweening is not installed.
    """
    x = ((x2 - x1) * n) + x1
    y = ((y2 - y1) * n) + y1
    return (x, y)


def linear(n):
    """
    Returns ``n``, where ``n`` is the float argument between ``0.0`` and ``1.0``. This function is for the default
    linear tween for mouse moving functions.

    This function was copied from PyTweening module, so that it can be called even if PyTweening is not installed.
    """

    # We use this function instead of pytweening.linear for the default tween function just in case pytweening couldn't be imported.
    if not 0.0 <= n <= 1.0:
        raise PyAutoGUIException("Argument must be between 0.0 and 1.0.")
    return n


def position(x=None, y=None):
    """
    Returns the current xy coordinates of the mouse cursor as a two-integer tuple.
    Args:
      x (int, None, optional) - If not None, this argument overrides the x in
        the return value.
      y (int, None, optional) - If not None, this argument overrides the y in
        the return value.
    Returns:
      (x, y) tuple of the current xy coordinates of the mouse cursor.
    NOTE: The position() function doesn't check for failsafe.
    """
    result = popen(
        "dbus-send --session --dest=com.deepin.Autotool --print-reply  /com/deepin/Autotool com.deepin.Autotool.getPos | grep double | awk \'{printf \"%d\\n\",$2}\'"
    ).split("\n")
    try:
        posx = int(result[0].strip())
        posy = int(result[1].strip())
    except ValueError as e:
        print(e)
        print(result)
        raise ValueError
    if x is not None:  # If set, the x parameter overrides the return value.
        posx = int(x)
    if y is not None:  # If set, the y parameter overrides the return value.
        posy = int(y)
    return Point(posx, posy)


def _normalizeXYArgs(firstArg, secondArg):
    """
    Returns a ``Point`` object based on ``firstArg`` and ``secondArg``, which are the first two arguments passed to
    several PyAutoGUI functions. If ``firstArg`` and ``secondArg`` are both ``None``, returns the current mouse cursor
    position.

    ``firstArg`` and ``secondArg`` can be integers, a sequence of integers, or a string representing an image filename
    to find on the screen (and return the center coordinates of).
    """
    if firstArg is None and secondArg is None:
        return position()
    else:
        return Point(firstArg, secondArg)


def size():
    result = popen(
        "dbus-send --session --dest=com.deepin.Autotool --print-reply  /com/deepin/Autotool com.deepin.Autotool.getSize | grep int32 | awk \'{printf \"%d\\n\",$2}\'"
    ).split("\n")
    posx = int(result[0].strip())
    posy = int(result[1].strip())
    if 0 == posx or 0 == posy:
        return size()
    return Size(posx, posy)


def moveTo(x=None, y=None, duration=0.0, tween=linear, logScreenshot=False, _pause=True):
    startx, starty = position()

    x = int(x) if x is not None else startx
    y = int(y) if y is not None else starty

    width, height = size()

    # Make sure x and y are within the screen bounds.
    # x = max(0, min(x, width - 1))
    # y = max(0, min(y, height - 1))

    # If the duration is small enough, just move the cursor there instantly.
    steps = [(x, y)]

    if duration > MINIMUM_DURATION:
        # Non-instant moving/dragging involves tweening:
        num_steps = max(width, height)
        sleep_amount = duration / num_steps
        if sleep_amount < MINIMUM_SLEEP:
            num_steps = int(duration / MINIMUM_SLEEP)
            sleep_amount = duration / num_steps
        # print(str(startx) + "," + str(starty))
        # print(str(x) + "," + str(y))
        steps = [getPointOnLine(startx, starty, x, y, tween(n / num_steps)) for n in range(num_steps)]
        # Making sure the last position is the actual destination.
        # print(steps)
        steps.append((x, y))
    # print(steps)
    for tweenX, tweenY in steps:
        if len(steps) > 1:
            # A single step does not require tweening.
            sleep(sleep_amount + 0.01)

        tweenX = int(round(tweenX))
        tweenY = int(round(tweenY))
        system(
            f"{dbus_cmd}.moveTo int32:{str(tweenX)} int32:{str(tweenY)}"
        )


def mouseDown(x=None, y=None, button=PRIMARY, duration=0.0, tween=linear, logScreenshot=None, _pause=True):
    x, y = _normalizeXYArgs(x, y)
    moveTo(x, y, duration, tween, logScreenshot, _pause)
    system(
        f"{dbus_cmd}.mouseDown string:{button}"
    )
    sleep(0.3)


def mouseUp(x=None, y=None, button=PRIMARY, duration=0.0, tween=linear, logScreenshot=None, _pause=True):
    x, y = _normalizeXYArgs(x, y)
    moveTo(x, y, duration, tween, logScreenshot, _pause)
    system(
        f"{dbus_cmd}.mouseUp string:{button}"
    )


def click(
        x=None, y=None, clicks=1, interval=0.0, button=PRIMARY, duration=0.0, tween=linear, logScreenshot=None,
        _pause=True
):
    x, y = _normalizeXYArgs(x, y)
    moveTo(x, y, duration, tween, logScreenshot, _pause)
    for i in range(clicks):
        if button in (LEFT, MIDDLE, RIGHT):
            system(
                f"{dbus_cmd}.click string:{button}"
            )
        sleep(interval)


def leftClick(x=None, y=None, interval=0.0, duration=0.0, tween=linear, logScreenshot=None, _pause=True):
    click(x, y, 1, interval, LEFT, duration, tween, logScreenshot, _pause=_pause)


def rightClick(x=None, y=None, interval=0.0, duration=0.0, tween=linear, logScreenshot=None, _pause=True):
    click(x, y, 1, interval, RIGHT, duration, tween, logScreenshot, _pause=_pause)


def middleClick(x=None, y=None, interval=0.0, duration=0.0, tween=linear, logScreenshot=None, _pause=True):
    click(x, y, 1, interval, MIDDLE, duration, tween, logScreenshot, _pause=_pause)


def doubleClick(x=None, y=None, interval=0.0, button=LEFT, duration=0.0, tween=linear, logScreenshot=None, _pause=True):
    click(x, y, 2, interval, button, duration, tween, logScreenshot, _pause=False)


def tripleClick(x=None, y=None, interval=0.0, button=LEFT, duration=0.0, tween=linear, logScreenshot=None, _pause=True):
    click(x, y, 3, interval, button, duration, tween, logScreenshot, _pause=False)


def scroll(clicks, x=None, y=None, logScreenshot=None, _pause=True):
    if type(x) in (tuple, list):
        x, y = x[0], x[1]
    x, y = position(x, y)
    moveTo(x, y)
    vscroll(clicks, x, y, logScreenshot, _pause)


def hscroll(clicks, x=None, y=None, logScreenshot=None, _pause=True):
    if type(x) in (tuple, list):
        x, y = x[0], x[1]
    x, y = position(x, y)
    moveTo(x, y)
    step = clicks / STEP_SLEEP
    for i in range(0, STEP_SLEEP):
        system(
            f"{dbus_cmd}.hscroll double:{str(-step)}"
        )
        sleep(0.05)


def vscroll(clicks, x=None, y=None, logScreenshot=None, _pause=True):
    if type(x) in (tuple, list):
        x, y = x[0], x[1]
    x, y = position(x, y)
    moveTo(x, y)
    step = clicks / STEP_SLEEP
    for i in range(0, STEP_SLEEP):
        system(
            f"{dbus_cmd}.vscroll double:{str(-step)}"
        )
        sleep(0.05)


def dragTo(
        x=None, y=None, duration=0.0, tween=linear, button=PRIMARY, logScreenshot=None, _pause=True, mouseDownUp=True
):
    x, y = _normalizeXYArgs(x, y)
    if mouseDownUp:
        mouseDown(button=button, logScreenshot=False, _pause=False)
    moveTo(x, y, duration, tween)
    if mouseDownUp:
        mouseUp(button=button, logScreenshot=False, _pause=False)


def dragRel(
        xOffset=0, yOffset=0, duration=0.0, tween=linear, button=PRIMARY, logScreenshot=None, _pause=True,
        mouseDownUp=True
):
    if xOffset is None:
        xOffset = 0
    if yOffset is None:
        yOffset = 0

    if type(xOffset) in (tuple, list):
        xOffset, yOffset = xOffset[0], xOffset[1]

    if xOffset == 0 and yOffset == 0:
        return  # no-op case

    mousex, mousey = position()
    mousex = mousex + xOffset
    mousey = mousey + mousey
    if mouseDownUp:
        mouseDown(button=button, logScreenshot=False, _pause=False)
    moveTo(mousex, mousey, duration, tween)
    if mouseDownUp:
        mouseUp(button=button, logScreenshot=False, _pause=False)


def keyDown(key, logScreenshot=None, _pause=True):
    global bshift
    try:
        if len(key) > 1:
            key = key.lower()
        if key in KEY_NAMES_S.keys():
            system(f"{dbus_cmd}.keyDown uint32:{str(KEY_NAMES['shiftleft'])}")
            bshift = True
        system(f"{dbus_cmd}.keyDown uint32:{str(KEY_NAMES[key])}")
    except Exception:
        if bshift == True:
            system(f"{dbus_cmd}.keyUp uint32:{str(KEY_NAMES['shiftleft'])}")
            bshift = False
        pass


def keyUp(key, logScreenshot=None, _pause=True):
    global bshift
    try:
        if len(key) > 1:
            key = key.lower()
        system(
            f"{dbus_cmd}.keyUp uint32:{str(KEY_NAMES[key])}"
        )
        if key in KEY_NAMES_S.keys():
            system(f"{dbus_cmd}.keyUp uint32:{str(KEY_NAMES['shiftleft'])}")
            bshift = False
    except Exception:
        if bshift == True:
            system(f"{dbus_cmd}.keyUp uint32:{str(KEY_NAMES['shiftleft'])}")
            bshift = False
        pass


def press(keys, presses=1, interval=0.0, logScreenshot=None, _pause=True):
    if type(keys) == str:
        if len(keys) > 1:
            keys = keys.lower()
        keys = [keys]  # If keys is 'enter', convert it to ['enter'].
    else:
        lowerKeys = []
        for s in keys:
            if len(s) > 1:
                lowerKeys.append(s.lower())
            else:
                lowerKeys.append(s)
        keys = lowerKeys
    interval = float(interval)
    for i in range(presses):
        for k in keys:
            keyDown(k)
            keyUp(k)
        sleep(interval)


def typewrite(message, interval=0.0, logScreenshot=None, _pause=True):
    interval = float(interval)  # TODO - this should be taken out.

    for c in message:
        if len(c) > 1:
            c = c.lower()
        press(c, _pause=False)
        sleep(interval)


write = typewrite  # In PyAutoGUI 1.0, write() replaces typewrite().


def hotkey(*args, **kwargs):
    """Performs key down presses on the arguments passed in order, then performs
    key releases in reverse order.

    The effect is that calling hotkey('ctrl', 'shift', 'c') would perform a
    "Ctrl-Shift-C" hotkey/keyboard shortcut press.

    Args:
      key(s) (str): The series of keys to press, in order. This can also be a
        list of key strings to press.
      interval (float, optional): The number of seconds in between each press.
        0.0 by default, for no pause in between presses.

    Returns:
      None
    """
    interval = float(kwargs.get("interval", 0.0))  # TODO - this should be taken out.

    for c in args:
        if len(c) > 1:
            c = c.lower()
        # print("keydown:" + c)
        keyDown(c)
        sleep(interval)
    for c in reversed(args):
        if len(c) > 1:
            c = c.lower()
        # print("keyup:" + c)
        keyUp(c)
        sleep(interval)


def screenshot():
    command = "dbus-send --session --print-reply --dest=org.kde.KWin /Screenshot org.kde.kwin.Screenshot.screenshotFullscreen"
    image_path = popen(command).strip().split("\n")[1].split("\"")[1].strip()
    # if image_path != "":
    #     image = Image.open(image_path)
    #     return image
    # else:
    #     return None
