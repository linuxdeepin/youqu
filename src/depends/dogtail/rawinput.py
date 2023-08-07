# -*- coding: utf-8 -*-

# This file was modified by UnionTech Software Technology Co., Ltd. in 2022/08/11

# pylint: disable=C0103,C0209,C0301,E1120,R0913,C0114,C0413,C0413,W0105,C0116,W0702,W0707,R1710,C0411,E0611
from __future__ import absolute_import, division, print_function, unicode_literals
from .config import config
from .utils import doDelay
from .logging import debugLogger as logger

if config.IS_WAYLAND:
    from . import rawinput_wayland
else:
    from pyatspi import Registry as registry
    from pyatspi import (KEY_SYM, KEY_PRESS, KEY_PRESSRELEASE, KEY_RELEASE)

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

"""
Handles raw input using AT-SPI event generation.

Note: Think of keyvals as keysyms, and keynames as keystrings.
"""
__author__ = """
David Malcolm <dmalcolm@redhat.com>,
Zack Cerza <zcerza@redhat.com>
"""


def doTypingDelay():
    doDelay(config.typingDelay)


def checkCoordinates(x, y):
    if x < 0 or y < 0:
        raise ValueError("Attempting to generate a mouse event at negative coordinates: (%s,%s)" % (x, y))


def click(x, y, button=1, check=True):
    """
    Synthesize a mouse button click at (x,y)
    """
    if check:
        checkCoordinates(x, y)
    logger.log("Mouse button %s click at (%s,%s)" % (button, x, y))
    if config.IS_X11:
        registry.generateMouseEvent(x, y, name='b%sc' % button)
    else:
        if button == 1:
            rawinput_wayland.leftClick(x, y)
        elif button == 2:
            rawinput_wayland.middleClick(x, y)
        elif button == 3:
            rawinput_wayland.rightClick(x, y)
        else:
            raise ValueError("参数 button 传入错误！")
    doDelay(config.actionDelay)


def point(x, y, check=True):
    if check:
        checkCoordinates(x, y)
    logger.log("Pointing mouse cursor at (%s,%s)" % (x, y))
    if config.IS_X11:
        registry.generateMouseEvent(x, y, 'abs')
    else:
        rawinput_wayland.moveTo(x, y)
    doDelay(config.actionDelay)


def doubleClick(x, y, button=1, check=True):
    """
    Synthesize a mouse button double-click at (x,y)
    """
    if check:
        checkCoordinates(x, y)
    logger.log("Mouse button %s doubleclick at (%s,%s)" % (button, x, y))
    if config.IS_X11:
        registry.generateMouseEvent(x, y, name='b%sd' % button)
    else:
        rawinput_wayland.doubleClick(x, y)
    doDelay()


def press(x, y, button=1, check=True):
    """
    Synthesize a mouse button press at (x,y)
    """
    if check:
        checkCoordinates(x, y)
    logger.log("Mouse button %s press at (%s,%s)" % (button, x, y))
    if config.IS_X11:
        registry.generateMouseEvent(x, y, name='b%sp' % button)
    else:
        rawinput_wayland.mouseDown(x, y)
    doDelay()


def release(x, y, button=1, check=True):
    """
    Synthesize a mouse button release at (x,y)
    """
    if check:
        checkCoordinates(x, y)
    logger.log("Mouse button %s release at (%s,%s)" % (button, x, y))
    if config.IS_X11:
        registry.generateMouseEvent(x, y, name='b%sr' % button)
    else:
        rawinput_wayland.mouseUp()
    doDelay()


def absoluteMotion(x, y, mouseDelay=None, check=True):
    """
    Synthesize mouse absolute motion to (x,y)
    """
    if check:
        checkCoordinates(x, y)
    logger.log("Mouse absolute motion to (%s,%s)" % (x, y))
    registry.generateMouseEvent(x, y, name='abs')
    if mouseDelay:
        doDelay(mouseDelay)
    else:
        doDelay()


def absoluteMotionWithTrajectory(source_x, source_y, dest_x, dest_y, mouseDelay=None, check=True):
    """
    Synthetize mouse absolute motion with trajectory. The 'trajectory' means that the whole motion
    is divided into several atomic movements which are synthetized separately.
    """
    if check:
        checkCoordinates(source_x, source_y)
        checkCoordinates(dest_x, dest_y)
    logger.log("Mouse absolute motion with trajectory to (%s,%s)" % (dest_x, dest_y))

    dx = float(dest_x - source_x)
    dy = float(dest_y - source_y)
    max_len = max(abs(dx), abs(dy))
    if max_len == 0:
        # actually, no motion requested
        return
    dx /= max_len
    dy /= max_len
    act_x = float(source_x)
    act_y = float(source_y)

    for _ in range(0, int(max_len)):
        act_x += dx
        act_y += dy
        if mouseDelay:
            doDelay(mouseDelay)
        registry.generateMouseEvent(int(act_x), int(act_y), name='abs')

    if mouseDelay:
        doDelay(mouseDelay)
    else:
        doDelay()


def relativeMotion(x, y, mouseDelay=None):
    """
    Synthetize a relative motion from actual position.
    Note: Does not check if the end coordinates are positive.
    """
    logger.log("Mouse relative motion of (%s,%s)" % (x, y))
    registry.generateMouseEvent(x, y, name='rel')
    if mouseDelay:
        doDelay(mouseDelay)
    else:
        doDelay()


def drag(fromXY, toXY, button=1, check=True):
    """
    Synthesize a mouse press, drag, and release on the screen.
    """
    logger.log("Mouse button %s drag from %s to %s" % (button, fromXY, toXY))

    (x, y) = fromXY
    press(x, y, button, check)

    (x, y) = toXY
    absoluteMotion(x, y, check=check)
    doDelay()

    release(x, y, button, check)
    doDelay()


def dragWithTrajectory(fromXY, toXY, button=1, check=True):
    """
    Synthetize a mouse press, drag (including move events), and release on the screen
    """
    logger.log("Mouse button %s drag with trajectory from %s to %s" % (button, fromXY, toXY))

    (x, y) = fromXY
    press(x, y, button, check)

    (x, y) = toXY
    absoluteMotionWithTrajectory(fromXY[0], fromXY[1], x, y, check=check)
    doDelay()

    release(x, y, button, check)
    doDelay()


def typeText(string):
    """
    Types the specified string, one character at a time.
    Please note, you may have to set a higher typing delay,
    if your machine misses/switches the characters typed.
    Needed sometimes on slow setups/VMs typing non-ASCII utf8 chars.
    """
    for char in string:
        pressKey(char)

keyNameAliases = {
    'enter': 'Return',
    'esc': 'Escape',
    'alt': 'Alt_L',
    'control': 'Control_L',
    'ctrl': 'Control_L',
    'shift': 'Shift_L',
    'del': 'Delete',
    'ins': 'Insert',
    'pageup': 'Page_Up',
    'pagedown': 'Page_Down',
    'win': 'Super_L',
    'meta': 'Super_L',
    'super': 'Super_L',
    ' ': 'space',
    '\t': 'Tab',
    '\n': 'Return'
}


def uniCharToKeySym(uniChar):
    i = ord(uniChar)
    keySym = Gdk.unicode_to_keyval(i)
    return keySym


def keyNameToKeySym(keyName):
    keyName = keyNameAliases.get(keyName.lower(), keyName)
    keySym = Gdk.keyval_from_name(keyName)
    # various error 'codes' returned for non-recognized chars in versions of GTK3.X
    if keySym == 0xffffff or keySym == 0x0 or keySym is None:
        try:
            keySym = uniCharToKeySym(keyName)
        except:  # not even valid utf-8 char
            try:  # Last attempt run at a keyName ('Meta_L', 'Dash' ...)
                keySym = getattr(Gdk, 'KEY_' + keyName)
            except AttributeError:
                raise KeyError(keyName)
    return keySym


def keyNameToKeyCode(keyName):
    """
    Use GDK to get the keycode for a given keystring.

    Note that the keycode returned by this function is often incorrect when
    the requested keystring is obtained by holding down the Shift key.

    Generally you should use uniCharToKeySym() and should only need this
    function for nonprintable keys anyway.
    """
    keymap = Gdk.Keymap.get_for_display(Gdk.Display.get_default())
    entries = keymap.get_entries_for_keyval(
        Gdk.keyval_from_name(keyName))
    try:
        return entries[1][0].keycode
    except TypeError:
        pass


def pressKey(keyName):
    """
    Presses (and releases) the key specified by keyName.
    keyName is the English name of the key as seen on the keyboard. Ex: 'enter'
    Names are looked up in Gdk.KEY_ If they are not found there, they are
    looked up by uniCharToKeySym().
    """
    keySym = keyNameToKeySym(keyName)
    registry.generateKeyboardEvent(keySym, None, KEY_SYM)
    doTypingDelay()


def keyCombo(comboString):
    """
    Generates the appropriate keyboard events to simulate a user pressing the
    specified key combination.

    comboString is the representation of the key combo to be generated.
    e.g. '<Control><Alt>p' or '<Control><Shift>PageUp' or '<Control>q'
    """
    strings = []
    for s in comboString.split('<'):
        if s:
            for S in s.split('>'):
                if S:
                    S = keyNameAliases.get(S.lower(), S)
                    strings.append(S)
    for s in strings:
        if not hasattr(Gdk, s):
            if not hasattr(Gdk, 'KEY_' + s):
                raise ValueError("Cannot find key %s" % s)
    modifiers = strings[:-1]
    finalKey = strings[-1]
    for modifier in modifiers:
        code = keyNameToKeyCode(modifier)
        registry.generateKeyboardEvent(code, None, KEY_PRESS)
    code = keyNameToKeyCode(finalKey)
    registry.generateKeyboardEvent(code, None, KEY_PRESSRELEASE)
    for modifier in modifiers:
        code = keyNameToKeyCode(modifier)
        registry.generateKeyboardEvent(code, None, KEY_RELEASE)
    doDelay()


def holdKey(keyName):
    code = keyNameToKeyCode(keyName)
    registry.generateKeyboardEvent(code, None, KEY_PRESS)
    doDelay()


def releaseKey(keyName):
    code = keyNameToKeyCode(keyName)
    registry.generateKeyboardEvent(code, None, KEY_RELEASE)
    doDelay()
