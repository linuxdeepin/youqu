# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from . import errors
from . import predicate
from . import rawinput
from . import tree
from .config import config
from .utils import Lock
import os

"""
Dogtail's procedural UI
All the classes here are intended to be single-instance, except for Action.
"""
__author__ = 'Zack Cerza <zcerza@redhat.com>'
#
#
# WARNING: Here There Be Dragons (TM)                                        #
#                                                                            #
# If you don't understand how to use this API, you almost certainly don't    #
# want to read the code first. We make use of some very non-intuitive        #
# features of Python in order to make the API very simplistic. Therefore,    #
# you should probably only read this code if you're already familiar with    #
# some of Python's advanced features. You have been warned. ;)               #
#
#


class FocusError(Exception):
    pass


def focusFailed(pred):
    errors.warn('The requested widget could not be focused: %s' % pred.debugName)

ENOARGS = "At least one argument is needed"


class FocusBase(object):
    """
    The base for every class in the module. Does nothing special, really.
    """
    node = None

    def __getattr__(self, name):
        # Fold all the Node's AT-SPI properties into the Focus object.
        try:
            return getattr(self.node, name)
        except AttributeError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        # Fold all the Node's AT-SPI properties into the Focus object.
        if name == 'node':
            setattr(self.__class__, name, value)
        else:
            try:
                setattr(self.node, name, value)
            except AttributeError:
                raise AttributeError(name)


class FocusApplication(FocusBase):
    """
    Keeps track of which application is currently focused.
    """
    desktop = tree.root

    def __call__(self, name):
        """
        Search for an application that matches and refocus on the given name.
        """
        try:
            pred = predicate.IsAnApplicationNamed(name)
            app = self.desktop.findChild(pred, recursive=False, retry=False)
        except tree.SearchError:
            if config.fatalErrors:
                raise FocusError(name)
            else:
                focusFailed(pred)
                return False
        if app:
            FocusApplication.node = app
            FocusDialog.node = None
            FocusWindow.node = None
            FocusWidget.node = None
        return True


class FocusDesktop(FocusBase):
    """
    This isn't used yet, and may never be used.
    """
    pass


class FocusWindow(FocusBase):
    """
    Keeps track of which window is currently focused.
    """

    def __call__(self, name):
        """
        Search for a dialog that matches the given name and refocus on it.
        """
        result = None
        pred = predicate.IsAWindowNamed(name)
        try:
            result = FocusApplication.node.findChild(pred, requireResult=False, recursive=False)
        except AttributeError:
            pass
        if result:
            FocusWindow.node = result
            FocusDialog.node = None
            FocusWidget.node = None
        else:
            if config.fatalErrors:
                raise FocusError(pred.debugName)
            else:
                focusFailed(pred)
                return False
        return True


class FocusDialog(FocusBase):
    """
    Keeps track of which dialog is currently focused.
    """

    def __call__(self, name):
        """
        Search for a dialog that matches the given name and refocus on it.
        """
        result = None
        pred = predicate.IsADialogNamed(name)
        try:
            result = FocusApplication.node.findChild(pred, requireResult=False, recursive=False)
        except AttributeError:
            pass
        if result:
            FocusDialog.node = result
            FocusWidget.node = None
        else:
            if config.fatalErrors:
                raise FocusError(pred.debugName)
            else:
                focusFailed(pred)
                return False
        return True


class FocusWidget(FocusBase):
    """
    Keeps track of which widget is currently focused.
    """

    def findByPredicate(self, pred):
        result = None
        try:
            result = FocusWidget.node.findChild(pred, requireResult=False, retry=False)
        except AttributeError:
            pass
        if result:
            FocusWidget.node = result
        else:
            try:
                result = FocusDialog.node.findChild(pred, requireResult=False, retry=False)
            except AttributeError:
                pass
        if result:
            FocusWidget.node = result
        else:
            try:
                result = FocusWindow.node.findChild(pred, requireResult=False, retry=False)
            except AttributeError:
                pass
        if result:
            FocusWidget.node = result
        else:
            try:
                result = FocusApplication.node.findChild(pred, requireResult=False, retry=False)
                if result:
                    FocusWidget.node = result
            except AttributeError:
                if config.fatalErrors:
                    raise FocusError(pred)
                else:
                    focusFailed(pred)
                    return False

        if result is None:
            FocusWidget.node = result
            if config.fatalErrors:
                raise FocusError(pred.debugName)
            else:
                focusFailed(pred)
                return False
        return True

    def __call__(self, name='', roleName='', description=''):
        """
        If name, roleName or description are specified, search for a widget that matches and refocus on it.
        """
        if not name and not roleName and not description:
            raise TypeError(ENOARGS)

        # search for a widget.
        pred = predicate.GenericPredicate(name=name, roleName=roleName, description=description)
        return self.findByPredicate(pred)


class Focus(FocusBase):
    """
    The container class for the focused application, dialog and widget.
    """

    def __getattr__(self, name):
        raise AttributeError(name)

    def __setattr__(self, name, value):
        if name in ('application', 'dialog', 'widget', 'window'):
            self.__dict__[name] = value
        else:
            raise AttributeError(name)

    desktop = tree.root
    application = FocusApplication()
    app = application  # shortcut :)
    dialog = FocusDialog()
    window = FocusWindow()
    frame = window
    widget = FocusWidget()

    def button(self, name):
        """
        A shortcut to self.widget.findByPredicate(predicate.IsAButtonNamed(name))
        """
        return self.widget.findByPredicate(predicate.IsAButtonNamed(name))

    def icon(self, name):
        """
        A shortcut to self.widget(name, roleName = 'icon')
        """
        return self.widget(name=name, roleName='icon')

    def menu(self, name):
        """
        A shortcut to self.widget.findByPredicate(predicate.IsAMenuNamed(name))
        """
        return self.widget.findByPredicate(predicate.IsAMenuNamed(name))

    def menuItem(self, name):
        """
        A shortcut to self.widget.findByPredicate(predicate.IsAMenuItemNamed(name))
        """
        return self.widget.findByPredicate(predicate.IsAMenuItemNamed(name))

    def table(self, name=''):
        """
        A shortcut to self.widget(name, roleName 'table')
        """
        return self.widget(name=name, roleName='table')

    def tableCell(self, name=''):
        """
        A shortcut to self.widget(name, roleName 'table cell')
        """
        return self.widget(name=name, roleName='table cell')

    def text(self, name=''):
        """
        A shortcut to self.widget.findByPredicate(IsATextEntryNamed(name))
        """
        return self.widget.findByPredicate(predicate.IsATextEntryNamed(name))


class Action(FocusWidget):
    """
    Aids in executing AT-SPI actions, refocusing the widget if necessary.
    """

    def __init__(self, action):
        """
        action is a string with the same name as the AT-SPI action you wish to execute using this class.
        """
        self.action = action

    def __call__(self, name='', roleName='', description='', delay=config.actionDelay):
        """
        If name, roleName or description are specified, first search for a widget that matches and refocus on it.
        Then execute the action.
        """
        if name or roleName or description:
            FocusWidget.__call__(self, name=name, roleName=roleName, description=description)
        self.node.doActionNamed(self.action)

    def __getattr__(self, attr):
        return getattr(FocusWidget.node, attr)

    def __setattr__(self, attr, value):
        if attr == 'action':
            self.__dict__[attr] = value
        else:
            setattr(FocusWidget, attr, value)

    def button(self, name):
        """
        A shortcut to self(name, roleName = 'push button')
        """
        self.__call__(name=name, roleName='push button')

    def menu(self, name):
        """
        A shortcut to self(name, roleName = 'menu')
        """
        self.__call__(name=name, roleName='menu')

    def menuItem(self, name):
        """
        A shortcut to self(name, roleName = 'menu item')
        """
        self.__call__(name=name, roleName='menu item')

    def table(self, name=''):
        """
        A shortcut to self(name, roleName 'table')
        """
        self.__call__(name=name, roleName='table')

    def tableCell(self, name=''):
        """
        A shortcut to self(name, roleName 'table cell')
        """
        self.__call__(name=name, roleName='table cell')

    def text(self, name=''):
        """
        A shortcut to self(name, roleName = 'text')
        """
        self.__call__(name=name, roleName='text')


class Click(Action):
    """
    A special case of Action, Click will eventually handle raw mouse events.
    """
    primary = 1
    middle = 2
    secondary = 3

    def __init__(self):
        Action.__init__(self, 'click')

    def __call__(self, name='', roleName='', description='', raw=True, button=primary, delay=config.actionDelay):
        """
        By default, execute a raw mouse event.
        If raw is False or if button evaluates to False, just pass the rest of
        the arguments to Action.
        """
        if name or roleName or description:
            FocusWidget.__call__(self, name=name, roleName=roleName, description=description)
        if raw and button:
            # We're doing a raw mouse click
            Click.node.click(button)
        else:
            Action.__call__(self, name=name, roleName=roleName, description=description, delay=delay)


class Select(Action):
    """
    Aids in selecting and deselecting widgets, i.e. page tabs
    """
    select = 'select'
    deselect = 'deselect'

    def __init__(self, action):
        """
        action must be 'select' or 'deselect'.
        """
        if action not in (self.select, self.deselect):
            raise ValueError(action)
        Action.__init__(self, action)

    def __call__(self, name='', roleName='', description='', delay=config.actionDelay):
        """
        If name, roleName or description are specified, first search for a widget that matches and refocus on it.
        Then execute the action.
        """
        if name or roleName or description:
            FocusWidget.__call__(self, name=name, roleName=roleName, description=description)
        func = getattr(self.node, self.action)
        func()


def type(text):
    if focus.widget.node:
        focus.widget.node.typeText(text)
    else:
        rawinput.typeText(text)


def keyCombo(combo):
    if focus.widget.node:
        focus.widget.node.keyCombo(combo)
    else:
        rawinput.keyCombo(combo)


def run(application, arguments='', appName=''):
    from .utils import run as utilsRun
    pid = utilsRun(application + ' ' + arguments, appName=appName)
    focus.application(application)
    return pid

# tell sniff not to use auto-refresh while script using this module is running
# may have already been locked by dogtail.tree
if not os.path.exists('/tmp/sniff_refresh.lock'):  # pragma: no cover
    # this lock will automatically unlock on script exit.
    sniff_lock = Lock(lockname='sniff_refresh.lock', randomize=False, unlockOnExit=True)
    try:
        sniff_lock.lock()
    except OSError:
        pass  # lock was already present from other script instance or leftover from killed instance

focus = Focus()
click = Click()
activate = Action('activate')
openItem = Action('open')
menu = Action('menu')
select = Select(Select.select)
deselect = Select(Select.deselect)
