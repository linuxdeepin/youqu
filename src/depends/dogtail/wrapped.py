# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import Accessibility

"""
Superclasses for application wrappers

Subclass these classes if you want to create application wrappers, e.g.:
http://svn.gnome.org/viewvc/dogtail-tests/trunk/appwrappers/dogtail/appwrappers/gedit.py?view=markup
"""
__author__ = "Zack Cerza <zcerza@redhat.com>"


def makeWrapperClass(wrappedClass, name):  # pragma: no cover
    class klass(object):

        def __init__(self, obj):
            self.obj = obj

        def __getattr__(self, name):
            if name == 'obj':
                return self.__dict__['obj']
            return getattr(self.obj, name)

        def __setattr__(self, name, value):
            if name == 'obj':
                self.__dict__['obj'] = value
            else:
                return setattr(self.obj, name, value)

    klass.__name__ = name
    return klass

Application = makeWrapperClass(Accessibility.Application, "WrappedApplication")
Node = makeWrapperClass(Accessibility.Accessible, "WrappedNode")
