# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

"""
Handles versioning of software packages
"""
__author__ = 'Dave Malcolm <dmalcolm@redhat.com>'


class Version(object):
    """
    Class representing a version of a software package.
    Stored internally as a list of subversions, from major to minor.
    Overloaded comparison operators ought to work sanely.
    """

    def __init__(self, versionList):
        self.versionList = versionList

    def fromString(versionString):
        """
        Parse a string of the form number.number.number
        """
        return Version(list(map(int, versionString.split("."))))
    fromString = staticmethod(fromString)

    def __str__(self):
        return ".".join(map(str, self.versionList))

    def __getNum(self):
        tmpList = list(self.versionList)

        while len(tmpList) < 5:
            tmpList += [0]

        num = 0
        for i in range(len(tmpList)):
            num *= 1000
            num += tmpList[i]
        return num

    def __lt__(self, other):
        return self.__getNum() < other.__getNum()

    def __le__(self, other):
        return self.__getNum() <= other.__getNum()

    def __eq__(self, other):
        return self.__getNum() == other.__getNum()

    def __ne__(self, other):
        return self.__getNum() != other.__getNum()

    def __gt__(self, other):
        return self.__getNum() > other.__getNum()

    def __ge__(self, other):
        return self.__getNum() >= other.__getNum()
