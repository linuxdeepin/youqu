# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from .config import config
import os
import sys
import time
import traceback

"""
Logging facilities
"""

__author__ = """Ed Rousseau <rousseau@redhat.com>,
Zack Cerza <zcerza@redhat.com,
David Malcolm <dmalcolm@redhat.com>
"""


class TimeStamp(object):
    """
    Timestamp class for file logs

    Generates timestamps tempfiles and log entries
    """
    def __init__(self):
        self.now = "0"
        self.timetup = time.localtime()

    def zeroPad(self, intt, width=2):
        """
        Pads an integer 'int' with zeroes, up to width 'width'.

        Returns a string.

        It will not truncate. If you call zeroPad(100, 2), '100' will be returned.
        """
        if intt < 10 ** width:
            return ("0" * (width - len(str(intt)))) + str(intt)
        else:
            return str(intt)

    # file stamper
    def fileStamp(self, filename, addTime=True):
        """
        Generates a filename stamp in the format of filename_YYYYMMDD-hhmmss.
        A format of filename_YYYYMMDD can be used instead by specifying addTime = False.
        """
        self.now = filename.strip() + "_"
        self.timetup = time.localtime()

        # Should produce rel-eng style filestamps
        # format it all pretty by chopping the tuple
        fieldCount = 3
        if addTime:
            fieldCount = fieldCount + 3
        for i in range(fieldCount):
            if i == 3:
                self.now = self.now + '-'
            self.now = self.now + self.zeroPad(self.timetup[i])
        return self.now

    # Log entry stamper
    def entryStamp(self):
        """
        Generates a logfile entry stamp of YYYY.MM.DD HH:MM:SS
        """
        self.timetup = time.localtime()

        # This will return a log entry formatted string in YYYY.MM.DD HH:MM:SS
        for i in range(6):
            # put in the year
            if i == 0:
                self.now = str(self.timetup[i])
            # Format Month and Day
            elif i == 1 or i == 2:
                self.now = self.now + "." + self.zeroPad(self.timetup[i])
            else:
                # make the " " between Day and Hour and put in the hour
                if i == 3:
                    self.now = self.now + " " + self.zeroPad(self.timetup[i])
                # Otherwise Use the ":" divider
                else:
                    self.now = self.now + ":" + self.zeroPad(self.timetup[i])
        return self.now


class Logger(object):
    """
    Writes entries to standard out.
    """
    stamper = TimeStamp()

    def __init__(self, logName, file=False, stdOut=True):
        """
        name: the name of the log
        file: The file object to log to.
        stdOut: Whether to log to standard out.
        """
        self.logName = logName
        self.stdOut = stdOut
        self.filee = file  # Handle to the logfile

        # store script name
        scriptName = config.scriptName

        # if script name is invalid, use the default one
        # most probably non-reachable code
        if not scriptName:  # pragma: no cover
            scriptName = 'log'

        # use script name as default filename
        self.fileName = scriptName

        # return if file is False or empty string
        # rewrite it for sure to False
        if not self.filee:
            self.filee = False
            return

        # check to see if we can write to the logDir
        if os.path.isdir(config.logDir):
            self.findUniqueName()
        else:
            # If path doesn't exist, raise an exception
            raise IOError("Log path %s does not exist or is not a directory" % config.logDir)

    def findUniqueName(self):
        """
        Generate a logfile name and check if it already exists to obtain a unique one
        """
        self.fileName = config.logDir + self.stamper.fileStamp(self.fileName) + '_' + self.logName
        i = 0

        # Iterate until self.fileName contains new unique file path
        while os.path.exists(self.fileName):
            # Append the file path with counter id
            if i == 0:
                self.fileName = self.fileName + "." + str(i)
            else:
                logsplit = self.fileName.split(".")
                logsplit[-1] = str(i)
                self.fileName = ".".join(logsplit)
            i += 1

    def createFile(self):
        """
        Try to create the file and write the header info
        """
        print("Creating logfile at %s ..." % self.fileName)
        self.filee = open(self.fileName, mode='w')
        self.filee.write("##### " + os.path.basename(self.fileName) + '\n')
        self.filee.flush()

    def log(self, message, newline=True, force=False):
        """
        Hook used for logging messages. Might eventually be a virtual
        function, but nice and simple for now.

        If force is True, log to a file irrespective of config.logDebugToFile.
        """

        # Create log file if file descriptor was not provided to constructor
        # and force or config.logDebugToFile is set to True
        if isinstance(self.filee, bool) and (force or config.logDebugToFile):
            self.createFile()

        # If force or config.logDebugToFile is set to True, write message to file
        if force or config.logDebugToFile:
            if newline:
                self.filee.write(message + str('\n'))
            else:
                self.filee.write(message + str(' '))
            self.filee.flush()

        # If both the self.stdOut and config.logDebugToStdOut are True, write to stdout
        if self.stdOut and config.logDebugToStdOut:
            try:
                print(message)
            except TypeError:
                print(message.decode('utf-8', 'replace'))


class ResultsLogger(Logger):
    """
    Writes entries into the Dogtail log
    """
    def __init__(self, stdOut=True):
        Logger.__init__(self, 'results', file=True, stdOut=stdOut)

    # Writes the result of a test case comparison to the log
    def log(self, entry):
        """
        Writes the log entry. Requires a 1 {key: value} pair dict for an argument or else it will
        throw an exception.
        """
        # We require a 1 key: value dict
        # Strip all leading and trailing witespace from entry dict and convert
        # to string for writing

        if len(entry) == 1:
            key = list(entry.keys())
            value = list(entry.values())
            key = key[0]
            value = value[0]
            entry = str(key) + ":      " + str(value)
        else:
            print("Method argument requires a 1 {key: value} dict. Supplied argument not one {key: value}")
            raise ValueError(entry)

        Logger.log(self, self.stamper.entryStamp() + "      " + entry, force=True)

debugLogger = Logger('debug', config.logDebugToFile)


def exceptionHook(exc, value, tb):  # pragma: no cover
    tbStringList = traceback.format_exception(exc, value, tb)
    tbString = ''.join(tbStringList)
    debugLogger.log(tbString)
    # sys.exc_clear()

sys.excepthook = exceptionHook
