# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

__author__ = """David Malcolm <dmalcolm@redhat.com>"""


class SearchPath(object):
    """
    Class used by the recording framework (and for more verbose script
    logging) for identifying nodes in a persistent way, independent of the
    style of script being written.

    Implemented as a list of (predicate, isRecursive) pairs, giving the
    'best' way to find the Accessible wrapped by a Node, starting at the
    root and applying each search in turn.

    This is somewhat analagous to an absolute path in a filesystem, except
    that some of searches may be recursive, rather than just searching
    direct children.

    FIXME: try to ensure uniqueness
    FIXME: need some heuristics to get 'good' searches, whatever
    that means
    """

    def __init__(self):
        self.lst = []

    def __str__(self):
        result = "{"
        for (predicate, isRecursive) in self.lst:
            result += "/(%s,%s)" % (predicate.describeSearchResult(), isRecursive)
        return result + "}"

    # We need equality to work so that dicts of these work:
    def __eq__(self, other):
        if len(self.lst) != len(other.lst):
            return False
        else:
            for i in range(len(self.lst)):
                if self.lst[i] != other.lst[i]:
                    return False
        return True

    def append(self, predicate, isRecursive):
        assert predicate
        self.lst.append((predicate, isRecursive))

    def __iter__(self):
        return iter(self.lst)

    def length(self):
        return len(self.lst)

    def makeScriptMethodCall(self):
        """
        Used by the recording system.

        Generate the Python source code that will carry out this search.
        """
        result = ""
        for (predicate, isRecursive) in self.lst:
            # print predicate
            # print self.generateVariableName(predicate)
            result += "." + predicate.makeScriptMethodCall(isRecursive)
        return result

    def getRelativePath(self, other):
        """
        Given another SearchPath instance, if the other is 'below' this
        one, return a SearchPath that describes how to reach it relative
        to this one (a copy of the second part of the list).    Otherwise
        return None.
        """
        i = 0
        for i in range(len(self.lst)):
            if self.lst[i] != other.lst[i]:
                break
        if i > 0:
            # Slice from this point to the end:
            result = SearchPath()
            result.lst = other.lst[i + 1:]

            if False:
                print("....................")
                print("from %s" % self)
                print("to %s" % other)
                print("i=%s" % i)
                print("relative path %s" % result)
                print("....................")

            return result
        else:
            return None

    def getPrefix(self, n):
        """
        Get the first n components of this instance as a new instance
        """
        result = SearchPath()
        for i in range(n):
            result.lst.append(self.lst[i])
        return result

    def getPredicate(self, i):
        (predicate, _) = self.lst[i]
        return predicate
