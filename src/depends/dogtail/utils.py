# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import os
import sys
import subprocess
import cairo
from . import predicate
import errno
import shlex

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, GLib
from .config import config
from time import sleep
from .logging import debugLogger as logger
from .logging import TimeStamp

"""
Various utilities
"""

__author__ = """Ed Rousseau <rousseau@redhat.com>,
Zack Cerza <zcerza@redhat.com,
David Malcolm <dmalcolm@redhat.com>
"""


def screenshot(file='screenshot.png', timeStamp=True):
    """
    This function wraps the ImageMagick import command to take a screenshot.

    The file argument may be specified as 'foo', 'foo.png', or using any other
    extension that ImageMagick supports. PNG is the default.

    By default, screenshot filenames are in the format of foo_YYYYMMDD-hhmmss.png .
    The timeStamp argument may be set to False to name the file foo.png.
    """
    if not isinstance(timeStamp, bool):
        raise TypeError("timeStampt must be True or False")
    # config is supposed to create this for us. If it's not there, bail.
    assert os.path.isdir(config.scratchDir)

    baseName = ''.join(file.split('.')[0:-1])
    fileExt = file.split('.')[-1].lower()
    if not baseName:
        baseName = file
        fileExt = 'png'

    if timeStamp:
        ts = TimeStamp()
        newFile = ts.fileStamp(baseName) + '.' + fileExt
        path = config.scratchDir + newFile
    else:
        newFile = baseName + '.' + fileExt
        path = config.scratchDir + newFile

    from gi.repository import Gdk
    from gi.repository import GdkPixbuf
    rootWindow = Gdk.get_default_root_window()
    geometry = rootWindow.get_geometry()
    pixbuf = GdkPixbuf.Pixbuf(colorspace=GdkPixbuf.Colorspace.RGB,
                              has_alpha=False,
                              bits_per_sample=8,
                              width=geometry[2],
                              height=geometry[3])

    pixbuf = Gdk.pixbuf_get_from_window(rootWindow, 0, 0, geometry[2], geometry[3])
    # GdkPixbuf.Pixbuf.save() needs 'jpeg' and not 'jpg'
    if fileExt == 'jpg':
        fileExt = 'jpeg'
    try:
        pixbuf.savev(path, fileExt, [], [])
    except GLib.GError:
        raise ValueError("Failed to save screenshot in %s format" % fileExt)
    assert os.path.exists(path)
    logger.log("Screenshot taken: " + path)
    return path


def run(string, timeout=config.runTimeout, interval=config.runInterval, desktop=None, dumb=False, appName=''):
    """
    Runs an application. [For simple command execution such as 'rm *', use os.popen() or os.system()]
    If dumb is omitted or is False, polls at interval seconds until the application is finished starting, or until
    timeout is reached.
    If dumb is True, returns when timeout is reached.
    """
    if not desktop:
        from dogtail.tree import root as desktop
    args = shlex.split(string)
    os.environ['GTK_MODULES'] = 'gail:atk-bridge'
    pid = subprocess.Popen(args, env=os.environ).pid

    if not appName:
        appName = args[0]

    if dumb:
        # We're starting a non-AT-SPI-aware application. Disable startup
        # detection.
        doDelay(timeout)
    else:
        # Startup detection code
        # The timing here is not totally precise, but it's good enough for now.
        time = 0
        while time < timeout:
            time = time + interval
            try:
                for child in desktop.children[::-1]:
                    if child.name == appName:
                        for grandchild in child.children:
                            if grandchild.roleName == 'frame':
                                from dogtail.procedural import focus
                                focus.application.node = child
                                doDelay(interval)
                                return pid
            except AttributeError:  # pragma: no cover
                pass
            doDelay(interval)
    return pid


def doDelay(delay=None):
    """
    Utility function to insert a delay (with logging and a configurable
    default delay)
    """
    if delay is None:
        delay = config.defaultDelay
    if config.debugSleep:
        logger.log("sleeping for %f" % delay)
    sleep(delay)


class Highlight (Gtk.Window):  # pragma: no cover

    def __init__(self, x, y, w, h):  # pragma: no cover
        super(Highlight, self).__init__()
        self.set_decorated(False)
        self.set_has_resize_grip(False)
        self.set_default_size(w, h)
        self.screen = self.get_screen()
        self.visual = self.screen.get_rgba_visual()
        if self.visual is not None and self.screen.is_composited():
            self.set_visual(self.visual)
        self.set_app_paintable(True)
        self.connect("draw", self.area_draw)
        self.show_all()
        self.move(x, y)

    def area_draw(self, widget, cr):  # pragma: no cover
        cr.set_source_rgba(.0, .0, .0, 0.0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)
        cr.set_source_rgb(0.9, 0.1, 0.1)
        cr.set_line_width(6)
        cr.rectangle(0, 0, self.get_size()[0], self.get_size()[1])
        cr.stroke()


class Blinker(object):  # pragma: no cover
    INTERVAL_MS = 1000
    main_loop = GLib.MainLoop()

    def __init__(self, x, y, w, h):  # pragma: no cover
        self.highlight_window = Highlight(x, y, w, h)
        if self.highlight_window.screen.is_composited() is not False:
            self.timeout_handler_id = GLib.timeout_add(
                Blinker.INTERVAL_MS, self.destroyHighlight)
            self.main_loop.run()
        else:
            self.highlight_window.destroy()

    def destroyHighlight(self):  # pragma: no cover
        self.highlight_window.destroy()
        self.main_loop.quit()
        return False


class Lock(object):
    """
    A known sytem-wide mutex implementation that uses atomicity of the mkdir operation in UNIX-like
    systems. This should be used mainly to provide mutual exclution in handling possible collisions
    among multiple script instances. You can choose to make randomized single-script wise locks
    or a more general locks if you do not choose to randomize the lockdir name. Set unLockOnExit
    to True to enable automatic unlock when scipt process exits to avoid having to unlock manually.
    """

    def __init__(self, location='/tmp', lockname='dogtail_lockdir_', randomize=True, unlockOnExit=False):
        """
        You can change the default lockdir location or name. Setting randomize to
        False will result in no random string being appened to the lockdir name.
        """
        self.lockdir = os.path.join(os.path.normpath(location), lockname)
        if randomize:
            self.lockdir = "%s%s" % (self.lockdir, self.__getPostfix())
        self.unlockOnExit = unlockOnExit

    def __exit_unlock(self):
        if os.path.exists(self.lockdir):
            try:
                os.rmdir(self.lockdir)
            except OSError:
                pass  # already deleted (by .unlock()), we're exiting, it's fine

    def lock(self):
        """
        Creates a lockdir based on the settings on Lock() instance creation.
        Raises OSError exception of the lock is already present. Should be
        atomic on POSIX compliant systems.
        """
        locked_msg = 'Dogtail lock: Already locked with the same lock'
        if not os.path.exists(self.lockdir):
            try:
                os.mkdir(self.lockdir)
            except OSError as e:
                if e.errno == errno.EEXIST and os.path.isdir(self.lockdir):
                    raise OSError(locked_msg)
            if os.path.exists(self.lockdir):
                if self.unlockOnExit:
                    import atexit
                    atexit.register(self.__exit_unlock)
                return self.lockdir
        else:
            raise OSError(locked_msg)

    def unlock(self):
        """
        Removes a lock. Will raise OSError exception if the lock was not present.
        Should be atomic on POSIX compliant systems.
        """
        #if self.unlockOnExit:
        #    raise Exception('Cannot unlock with unlockOnExit set to True!')
        if os.path.exists(self.lockdir):
            try:
                os.rmdir(self.lockdir)
            except OSError as e:
                if e.erron == errno.EEXIST:
                    raise OSError('Dogtail unlock: lockdir removed elsewhere!')
        else:
            raise OSError('Dogtail unlock: not locked')

    def locked(self):
        return os.path.exists(self.lockdir)

    def __getPostfix(self):
        import random
        import string
        return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(5))


a11yDConfKey = 'org.gnome.desktop.interface'


def isA11yEnabled():
    """
    Checks if accessibility is enabled via DConf.
    """
    from gi.repository.Gio import Settings
    try:
        InterfaceSettings = Settings(schema_id=a11yDConfKey)
    except TypeError: # if we have older glib that has deprecated param name
        InterfaceSettings = Settings(schema=a11yDConfKey)
    dconfEnabled = InterfaceSettings.get_boolean('toolkit-accessibility')
    if os.environ.get('GTK_MODULES', '').find('gail:atk-bridge') == -1:
        envEnabled = False
    else:
        envEnabled = True  # pragma: no cover
    return (dconfEnabled or envEnabled)


def bailBecauseA11yIsDisabled():
    if sys.argv[0].endswith("pydoc"):
        return
    try:
        with open("/proc/%s/cmdline" % os.getpid(), 'r') as f:
            content = f.read()
        if content.find('epydoc') != -1:
            return  # pragma: no cover
        if content.find('sphinx') != -1:
            return  # pragma: no cover
    except:   # pragma: no cover
        pass  # pragma: no cover
    logger.log("Dogtail requires that Assistive Technology support be enabled."
               "\nYou can enable accessibility with sniff or by running:\n"
               "'gsettings set org.gnome.desktop.interface toolkit-accessibility true'\nAborting...")
    sys.exit(1)


def enableA11y(enable=True):
    """
    Enables accessibility via DConf.
    """
    from gi.repository.Gio import Settings
    InterfaceSettings = Settings(schema_id=a11yDConfKey)
    InterfaceSettings.set_boolean('toolkit-accessibility', enable)


def checkForA11y():
    """
    Checks if accessibility is enabled, and halts execution if it is not.
    """
    if not isA11yEnabled():  # pragma: no cover
        bailBecauseA11yIsDisabled()


def checkForA11yInteractively():  # pragma: no cover
    """
    Checks if accessibility is enabled, and presents a dialog prompting the
    user if it should be enabled if it is not already, then halts execution.
    """
    if isA11yEnabled():
        return
    dialog = Gtk.Dialog('Enable Assistive Technology Support?',
                        None,
                        Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                        (Gtk.STOCK_QUIT, Gtk.ResponseType.CLOSE,
                         "_Enable", Gtk.ResponseType.ACCEPT))
    question = """Dogtail requires that Assistive Technology Support be enabled for it to function. Would you like to
enable Assistive Technology support now?

Note that you will have to log out for the change to fully take effect.
    """.strip()
    dialog.set_default_response(Gtk.ResponseType.ACCEPT)
    questionLabel = Gtk.Label(label=question)
    questionLabel.set_line_wrap(True)
    dialog.vbox.pack_start(questionLabel, True, True, 0)
    dialog.show_all()
    result = dialog.run()
    if result == Gtk.ResponseType.ACCEPT:
        logger.log("Enabling accessibility...")
        enableA11y()
    elif result == Gtk.ResponseType.CLOSE:
        bailBecauseA11yIsDisabled()
    dialog.destroy()


class GnomeShell(object):  # pragma: no cover

    """
    Utility class to help working with certain atributes of gnome-shell.
    Currently that means handling the Application menu available for apps
    on the top gnome-shell panel. Searching for the menu and its items is
    somewhat tricky due to fuzzy a11y tree of gnome-shell, mainly since the
    actual menu is not present as child to the menu-spawning button. Also,
    the menus get constructed/destroyed on the fly with application focus
    changes. Thus current application name as displayed plus a reference
    known menu item (with 'Quit' as default) are required by these methods.
    """

    def __init__(self, classic_mode=False):
        from dogtail.tree import root
        self.shell = root.application('gnome-shell')

    def getApplicationMenuList(self, search_by_item='Quit'):
        """
        Returns list of all menu item nodes. Searches for the menu by a reference item.
        Provide a different item name, if the 'Quit' is not present - but beware picking one
        present elsewhere, like 'Lock' or 'Power Off' present under the user menu.
        """
        matches = self.shell.findChildren(
            predicate.GenericPredicate(name=search_by_item, roleName='label'))
        for match in matches:
            ancestor = match.parent.parent.parent
            if ancestor.roleName == 'panel':
                return ancestor.findChildren(predicate.GenericPredicate(roleName='label'))
        from dogtail.tree import SearchError
        raise SearchError(
            "Could not find the Application menu based on '%s' item. Please provide an existing reference item"
            % search_by_item)

    def getApplicationMenuButton(self, app_name):
        """
        Returns the application menu 'button' node as present on the gnome-shell top panel.
        """
        try:
            return self.shell[0][0][3].child(app_name, roleName='label')
        except:
            from dogtail.tree import SearchError
            raise SearchError(
                "Application menu button of %s could not be found within gnome-shell!" % app_name)

    def getApplicationMenuItem(self, item, search_by_item='Quit'):
        """
        Returns a particilar menu item node. Uses a different 'Quit' or custom item name for reference, but also
        attempts to use the given item if the general reference fails.
        """
        try:
            menu_items = self.getApplicationMenuList(search_by_item)
        except:
            menu_items = self.getApplicationMenuList(item)
        if any(ord(x) > 127 for x in item):
            item = item.encode('utf-8')
        for node in menu_items:
            if node.name == item:
                return node
        raise Exception(
            'Could not find the item, did application focus change?')

    def clickApplicationMenuItem(self, app_name, item, search_by_item='Quit'):
        """
        Executes the given menu item through opening the menu first followed
        by a click at the particular item. The menu search reference 'Quit'
        may be customized. Also attempts to use the given item for reference
        if search fails with the default/custom one.
        """

        # a problem with this version of GS misreporting the positions
        from subprocess import check_output
        if 'Fedora release 25' in check_output('cat /etc/redhat-release', shell=True):
            xoffset = -130
            from dogtail.rawinput import click
            nd = self.getApplicationMenuButton(app_name)
            x = nd.position[0] + nd.size[0] / 2 + xoffset
            y = nd.position[1] + nd.size[1] / 2
            click(x, y)
            nd = self.getApplicationMenuItem(item, search_by_item)
            x = nd.position[0] + nd.size[0] / 2 + xoffset
            y = nd.position[1] + nd.size[1] / 2
            click(x, y)
        else:
            self.getApplicationMenuButton(app_name).click()
            self.getApplicationMenuItem(item, search_by_item).click()
