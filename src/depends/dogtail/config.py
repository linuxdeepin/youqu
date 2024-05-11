# -*- coding: utf-8 -*-
# This file was modified by UnionTech Software Technology Co., Ltd. in 2022/08/11
# pylint: disable=C0114,W0105,C0103,R0205,C0116,R1720,C0415，W0707,C0209,R0202,C0115,R0903,C0301
from __future__ import absolute_import, division, print_function, unicode_literals
import locale
import os
import sys
import pwd

"""
The configuration module.
"""
__author__ = "Zack Cerza <zcerza@redhat.com>, David Malcolm <dmalcolm@redhat.com>"


def _userTmpDir(baseName):
    # i.e. /tmp/dogtail-foo
    logname = os.getenv('LOGNAME', default=pwd.getpwuid(os.getuid())[0])
    return '-'.join(('/'.join(('/tmp', baseName)), logname))


class _Config(object):

    """
    Contains configuration parameters for the dogtail run.

    scratchDir(str):
    Directory where things like screenshots are stored.

    dataDir(str):
    Directory where related data files are located.

    logDir(str):
    Directory where dogtail.tc.TC*-generated logs are stored.

    scriptName(str) [Read-Only]:
    The name of the script being run.

    encoding(str)
    The encoding for text, used by dogtail.tc.TCString .

    actionDelay(float):
    The delay after an action is executed.

    typingDelay(float):
    The delay after a character is typed on the keyboard.

    runInterval(float):
    The interval at which dogtail.utils.run() and dogtail.procedural.run()
    check to see if the application has started up.

    runTimeout(int):
    The timeout after which dogtail.utils.run() and dogtail.procedural.run()
    give up on looking for the newly-started application.

    searchBackoffDuration (float):
    Time in seconds for which to delay when a search fails.

    searchWarningThreshold (int):
    Number of retries before logging the individual attempts at a search.

    searchCutoffCount (int):
    Number of times to retry when a search fails.

    searchShowingOnly (boolean):
    Whether to only search among nodes that are currently being shown.

    defaultDelay (float):
    Default time in seconds to sleep when delaying.

    childrenLimit (int):
    When there are a very large number of children of a node, only return
    this many, starting with the first.

    debugSearching (boolean):
    Whether to write info on search backoff and retry to the debug log.

    debugSleep (boolean):
    Whether to log whenever we sleep to the debug log.

    debugSearchPaths (boolean):
    Whether we should write out debug info when running the SearchPath
    routines.

    absoluteNodePaths (boolean):
    Whether we should identify nodes in the logs with long 'abcolute paths', or
    merely with a short 'relative path'. FIXME: give examples

    ensureSensitivity (boolean):
    Should we check that ui nodes are sensitive (not 'greyed out') before
    performing actions on them? If this is True (the default) it will raise
    an exception if this happens. Can set to False as a workaround for apps
    and toolkits that don't report sensitivity properly.

    debugTranslation (boolean):
    Whether we should write out debug information from the translation/i18n
    subsystem.

    blinkOnActions (boolean):
    Whether we should blink a rectangle around a Node when an action is
    performed on it.

    fatalErrors (boolean):
    Whether errors encountered in dogtail.procedural should be considered
    fatal. If True, exceptions will be raised. If False, warnings will be
    passed to the debug logger.

    checkForA11y (boolean):
    Whether to check if accessibility is enabled. If not, just assume it is
    (default True).

    logDebugToFile (boolean):
    Whether to write debug output to a log file.

    logDebugToStdOut (boolean):
    Whether to print log output to console or not (default True).

    reversed (boolean):
    When traversing nodes, is reverse iteration adopted?(default False).

    """
    @property
    def scriptName(self):
        return os.path.basename(sys.argv[0]).replace('.py', '')

    @property
    def encoding(self):
        return locale.getpreferredencoding().lower()

    defaults = {
        # Storage
        'scratchDir': '/'.join((_userTmpDir('dogtail'), '')),
        'dataDir': '/'.join((_userTmpDir('dogtail'), 'data', '')),
        'logDir': '/'.join((_userTmpDir('dogtail'), 'logs', '')),
        'scriptName': scriptName.fget(None),
        'encoding': encoding.fget(None),
        'configFile': None,
        'baseFile': None,

        # Timing and Limits
        'actionDelay': 1.0,
        'typingDelay': 0.1,
        'runInterval': 0.5,
        'runTimeout': 30,
        'searchBackoffDuration': 0.5,
        'searchWarningThreshold': 3,
        'searchCutoffCount': 20,
        'searchShowingOnly': False,
        'defaultDelay': 0.5,
        'childrenLimit': 100,

        # Debug
        'debugSearching': False,
        'debugSleep': False,
        'debugSearchPaths': False,
        'logDebugToStdOut': True,
        'absoluteNodePaths': False,
        'ensureSensitivity': False,
        'debugTranslation': False,
        'blinkOnActions': False,
        'fatalErrors': False,
        'checkForA11y': True,

        # Logging
        'logDebugToFile': True,

        # reversed
        'reversed': True
    }

    options = {}

    invalidValue = "__INVALID__"

    def __init__(self):
        _Config.__createDir(_Config.defaults['scratchDir'])
        _Config.__createDir(_Config.defaults['logDir'])
        _Config.__createDir(_Config.defaults['dataDir'])

    def __setattr__(self, name, value):
        if name not in config.defaults:
            raise AttributeError(name + " is not a valid option.")

        elif _Config.defaults[name] != value or \
                _Config.options.get(name, _Config.invalidValue) != value:
            if 'Dir' in name:
                _Config.__createDir(value)
                if value[-1] != os.path.sep:
                    value = value + os.path.sep
            elif name == 'logDebugToFile':
                from . import logging
                logging.debugLogger = logging.Logger('debug', value)
            _Config.options[name] = value

    def __getattr__(self, name):
        try:
            return _Config.options[name]
        except KeyError:
            try:
                return _Config.defaults[name]
            except KeyError:
                raise AttributeError("%s is not a valid option." % name)

    def __createDir(cls, dirName, perms=0o777):
        """
        Creates a directory (if it doesn't currently exist), creating any
        parent directories it needs.

        If perms is None, create with python's default permissions.
        """
        dirName = os.path.abspath(dirName)
        # print "Checking for %s ..." % dirName,
        if not os.path.isdir(dirName):
            if perms:
                umask = os.umask(0)
                os.makedirs(dirName, perms)
                os.umask(umask)
            else:
                # This is probably a dead code - no other functions call this without the
                # permissions set
                os.makedirs(dirName)  # pragma: no cover
    __createDir = classmethod(__createDir)

    def load(self, dictt):
        """
        Loads values from dict, preserving any options already set that are not overridden.
        """
        _Config.options.update(dictt)

    def reset(self):
        """
        Resets all settings to their defaults.
        """
        _Config.options = {}

        # 显示服务器

    DISPLAY_SERVER = (
                         os.popen("cat ~/.xsession-errors | grep XDG_SESSION_TYPE | head -n 1")
                             .read()
                             .split("=")[-1]
                             .strip("\n")
                     ) or ("x11" if os.popen("ps -ef | grep -v grep | grep kwin_x11").read() else "wayland")

    class DisplayServer:
        wayland = "wayland"
        x11 = "x11"

    IS_X11 = (DISPLAY_SERVER == DisplayServer.x11)
    IS_WAYLAND = (DISPLAY_SERVER == DisplayServer.wayland)


config = _Config()
