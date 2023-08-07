# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from .config import config
from .logging import ResultsLogger

"""
Test Case magic

FIXME: This module has not been tested since while. Use it with caution!
(and even better - avoid it and use dogtail.tree)
"""
__author__ = "Ed Rousseau <rousseau@redhat.com>"


class TC(object):  # pragma: no cover
    """
    The Test Case Superclass
    """
    logger = ResultsLogger()

    def __init__(self):
        self.encoding = config.encoding
        # ascii + unicode. 8 bit extended char has been ripped out
        self.supportedtypes = (
            "ascii", "utf-8", "utf-16", "utf-16-be", "utf-16-le", "unicode-escape", "raw-unicode-escape",
            "big5", "gb18030", "eucJP", "eucKR", "shiftJIS")

    # String comparison function
    def compare(self, label, baseline, undertest, encoding=config.encoding):
        """
        Compares 2 strings to see if they are the same. The user may specify
        the encoding to which the two strings are to be normalized for the
        comparison. Default encoding is the default system encoding.
        Normalization to extended 8 bit charactersets is not supported.

        When the origin of either baseline or undertest is a text file whose
        encoding is something other than ASCII, it is necessary to use
        codecs.open() instead of open(), so the file's encoding may be
        specified.
        """
        self.label = label.strip()
        self.baseline = baseline
        self.undertest = undertest
        for string in [self.baseline, self.undertest]:
            try:
                string = str(string, 'utf-8')
            except TypeError:
                pass
        self.encoding = encoding

        # Normalize the encoding type for the comparaison based on
        # self.encoding
        if self.encoding in self.supportedtypes:
            self.baseline = (self.baseline).encode(self.encoding)
            self.undertest = (self.undertest).encode(self.encoding)
            # Compare the strings
            if self.baseline == self.undertest:
                self.result = {self.label: "Passed"}
            else:
                self.result = {self.label: "Failed - " + self.encoding +
                               " strings do not match. " + self.baseline +
                               " expected: Got " + self.undertest}
            # Pass the test result to the ResultsLogger for writing
            TC.logger.log(self.result)
            return self.result

        else:
            # We should probably raise an exception here
            self.result = {
                self.label: "ERROR - " + self.encoding + " is not a supported encoding type"}
            TC.logger.log(self.result)
            return self.result


# String Test Case subclass
class TCString(TC):  # pragma: no cover
    """
    String Test Case Class
    """

    def __init__(self):
        TC.__init__(self)


# TODO: rewrite to Python3 compatible image library
#from PIL import Image, ImageChops, ImageStat
# TODO: rewrite to Python3 compatible image library OR remove
# Image test case subclass
#class TCImage(TC):  # pragma: no cover
#
#    """
#    Image Test Case Class.
#    """
#
#    def compare(self, label, baseline, undertest):
#        for _file in (baseline, undertest):
#            if type(_file) is not str and type(_file) is not str:
#                raise TypeError("Need filenames!")
#        self.label = label.strip()
#        self.baseline = baseline.strip()
#        self.undertest = undertest.strip()
#        diffName = TimeStamp().fileStamp("diff") + ".png"
#        self.diff = os.path.normpath(
#            os.path.sep.join((config.scratchDir, diffName)))
#
#        self.baseImage = Image.open(self.baseline)
#        self.testImage = Image.open(self.undertest)
#        try:
#            if self.baseImage.size != self.testImage.size:
#                self.result = {
#                    self.label: "Failed - images are different sizes"}
#                raise StopIteration
#
#            self.diffImage = ImageChops.difference(self.baseImage,
#                                                   self.testImage)
#            self.diffImage.save(self.diff)
#            result = False
#            for stat in ('stddev', 'mean', 'sum2'):
#                for item in getattr(ImageStat.Stat(self.diffImage), stat):
#                    if item:
#                        self.result = {self.label: "Failed - see %s" %
#                                       self.diff}
#                        raise StopIteration
#                    else:
#                        result = True
#        except StopIteration:
#            result = False
#
#        if result:
#            self.result = {self.label: "Passed"}
#
#        TC.logger.log(self.result)
#        return self.result


class TCNumber(TC):
    """
    Number Comparaison Test Case Class
    """

    def __init__(self):
        TC.__init__(self)
        self.supportedtypes = ("int", "float", "complex", "oct", "hex")

    # Compare 2 numbers by the type provided in the type arg
    def compare(self, label, baseline, undertest, type):
        """
        Compares 2 numbers to see if they are the same. The user may specify
        how to normalize mixed type comparisons via the type argument.
        """
        self.label = label.strip()
        self.baseline = baseline
        self.undertest = undertest
        self.type = type.strip()

        # If we get a valid type, convert to that type and compare
        if self.type in self.supportedtypes:
            # Normalize for comparison
            if self.type == "int":
                self.baseline = int(self.baseline)
                self.undertest = int(self.undertest)
            elif self.type == "float":
                self.baseline = float(self.baseline)
                self.undertest = float(self.undertest)
            else:
                self.baseline = complex(self.baseline)
                self.undertest = complex(self.undertest)

            # compare
            if self.baseline == self.undertest:
                self.result = {self.label: "Passed - numbers are the same"}
            else:
                self.result = {self.label: "Failed - " + str(
                    self.baseline) + " expected: Got " + str(self.undertest)}
            TC.logger.log(self.result)
            return self.result
        else:
            self.result = {
                self.label: "Failed - " + self.type + " is not in list of supported types"}
            TC.logger.log(self.result)
            return self.result


class TCBool(TC):  # pragma: no cover

    def __init__(self):
        pass

    def compare(self, label, _bool):
        """
        If _bool is True, pass.
        If _bool is False, fail.
        """
        if type(_bool) is not bool:
            raise TypeError
        if _bool:
            result = {label: "Passed"}
        else:
            result = {label: "Failed"}
        TC.logger.log(result)

from dogtail.tree import Node


class TCNode(TC):  # pragma: no cover

    def __init__(self):
        pass

    def compare(self, label, baseline, undertest):
        """
        If baseline is None, simply check that undertest is a Node.
        If baseline is a Node, check that it is equal to undertest.
        """
        if baseline is not None and not isinstance(baseline, Node):
            raise TypeError

        if not isinstance(undertest, Node):
            result = {label: "Failed - %s is not a Node" % undertest}
        elif baseline is None:
            result = {label: "Passed - %s is a Node" % undertest}
        elif isinstance(baseline, Node):
            if baseline == undertest:
                result = {label: "Passed - %s == %s" % (baseline, undertest)}
            else:
                result = {label: "Failed - %s != %s" % (baseline, undertest)}
        TC.logger.log(result)
