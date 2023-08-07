# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from . import config
import os
import re
import gettext
from .logging import debugLogger as logger

"""
Internationalization facilities
"""
__author__ = """David Malcolm <dmalcolm@redhat.com>, Zack Cerza <zcerza@redhat.com>"""


"""
Singleton list of TranslationDb instances, to be initialized by the script with
whatever translation databases it wants.
"""
translationDbs = []


class TranslationDb(object):
    """
    Abstract base class representing a database of translations
    """
    def getTranslationsOf(self, srcName):
        """
        Pure virtual method to look up the translation of a string.
        Returns a list of candidate strings (the translation), empty if not found.

        Note that a source string can map to multiple translated strings. For
        example, in the French translation of Evolution, the string "Forward" can
        translate to both
        (i) "Faire suivre" for forwarding an email, and
        (ii) "Suivant" for the next page in a wizard.
        """
        raise NotImplementedError


class GettextTranslationDb(TranslationDb):
    """
    Implementation of TranslationDb which leverages gettext, using a single
    translation mo-file.
    """
    def __init__(self, moFile):
        self.__moFile = moFile
        self.__gnutranslations = gettext.GNUTranslations(open(moFile))

    def getTranslationsOf(self, srcName):
        # print "searching for translations of %s"%srcName
        # Use a dict to get uniqueness:
        results = {}
        result = self.__gnutranslations.ugettext(srcName)
        if result != srcName:
            results[result] = None

        # Hack alert:
        #
        # Note that typical UI definition in GTK etc contains strings with
        # underscores to denote accelerators.
        # For example, the stock GTK "Add" item has text "_Add" which e.g.
        # translates to "A_jouter" in French
        #
        # Since these underscores have been stripped out before we see these strings,
        # we are looking for a translation of "Add" into "Ajouter" in this case, so
        # we need to fake it, by looking up the string multiple times, with underscores
        # inserted in all possible positions, stripping underscores out of the result.
        # Ugly, but it works.

        for index in range(len(srcName)):
            candidate = srcName[:index] + "_" + srcName[index:]
            result = self.__gnutranslations.ugettext(candidate)
            if result != candidate:
                # Strip out the underscore, and add to the result:
                results[result.replace('_', '')] = True

        return list(results.keys())


def translate(srcString):
    """
    Look up srcString in the various translation databases (if any), returning
    a list of all matches found (potentially the empty list)
    """
    # Use a dict to get uniqueness:
    results = {}
    # Try to translate the string:
    for translationDb in translationDbs:
        for result in translationDb.getTranslationsOf(srcString):
            results[result] = True

    # No translations found:
    if len(results) == 0:
        if config.config.debugTranslation:
            logger.log('Translation not found for "%s"' % srcString)
    return list(results.keys())


class TranslatableString(object):
    """
    Class representing a string that we want to match strings against, handling
    translation for us, by looking it up once at construction time.
    """

    def __init__(self, untranslatedString):
        """
        Constructor looks up the string in all of the translation databases, storing
        the various translations it finds.
        """
        try:  # python3 to get a plain always unicode string
            self.untranslatedString = str(untranslatedString)
        except UnicodeEncodeError:  # python2 to get non-unicode string for search comparions
            self.untranslatedString = untranslatedString.encode('utf-8')
        self.translatedStrings = translate(untranslatedString)

    def matchedBy(self, string):
        """
        Compare the test string against either the translation of the original
        string (or simply the original string, if no translation was found).
        """
        def stringsMatch(inS, outS):
            """
            Compares a regular expression to a string

            inS: the regular expression (or normal string)
            outS: the normal string to be compared against
            """
            inString = str(inS)
            outString = outS
            if inString == outString:
                return True
            inString = inString + '$'
            if inString[0] == '*':
                inString = "\\" + inString
            # Escape all parentheses, since grouping will never be needed here
            inString = re.sub('([\(\)])', r'\\\1', inString)
            match = re.match(inString, outString)
            matched = match is not None
            return matched

        matched = False
        # the 'ts' variable keeps track of whether we're working with
        # translated strings. it's only used for debugging purposes.
        #ts = 0
        # print string, str(self)
        for translatedString in self.translatedStrings:
            #ts = ts + 1
            matched = stringsMatch(translatedString, string)
            if not matched:
                matched = translatedString == string
            if matched:
                return matched
        # ts=0
        return stringsMatch(self.untranslatedString, string)

    def __str__(self):
        """
        Provide a meaningful debug version of the string (and the translation in
        use)
        """
        if len(self.translatedStrings) > 0:
            # build an output string, with commas in the correct places
            translations = ""
            for tString in self.translatedStrings:
                translations += '"%s", ' % tString
            result = '"%s" (%s)' % (
                self.untranslatedString, translations)
            return result
        else:
            return str('"%s"') % self.untranslatedString


def isMoFile(filename, language=''):
    """
    Does the given filename look like a gettext mo file?

    Optionally: Does the file also contain translations for a certain language,
    for example 'ja'?
    """
    if re.match('(.*)\\.mo$', filename):
        if not language:
            return True
        elif re.match('/usr/share/locale(.*)/%s(.*)/LC_MESSAGES/(.*)\\.mo$' % language, filename):
            return True
        else:
            return False
    else:
        return False


def loadAllTranslationsForLanguage(language):
    from dogtail import distro
    for moFile in distro.packageDb.getMoFiles(language):
        translationDbs.append(GettextTranslationDb(moFile))


def getMoFilesForPackage(packageName, language='', getDependencies=True):
    """
    Look up the named package and find all gettext mo files within it and its
    dependencies. It is possible to restrict the results to those of a certain
    language, for example 'ja'.
    """
    from dogtail import distro

    result = []
    for filename in distro.packageDb.getFiles(packageName):
        if isMoFile(filename, language):
            result.append(filename)

    if getDependencies:
        # Recurse:
        for dep in distro.packageDb.getDependencies(packageName):
            # We pass False to the inner call because getDependencies has already
            # walked the full tree
            result.extend(getMoFilesForPackage(dep, language, False))

    return result


def loadTranslationsFromPackageMoFiles(packageName, getDependencies=True):
    """
    Helper function which appends all of the gettext translation mo-files used by
    the package (and its dependencies) to the translation database list.
    """
    # Keep a list of mo-files that are already in use to avoid duplicates.
    moFiles = {}

    def load(packageName, language='', getDependencies=True):
        for moFile in getMoFilesForPackage(packageName, language, getDependencies):
            # Searching the popt mo-files for translations makes gettext bail out,
            # so we ignore them here. This is
            # https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=172155 .
            if not('popt.mo' in moFile or moFile in moFiles):
                try:
                    translationDbs.append(GettextTranslationDb(moFile))
                    moFiles[moFile] = None
                except (AttributeError, IndexError):
                    if config.config.debugTranslation:
                        #import traceback
                        # logger.log(traceback.format_exc())
                        logger.log("Warning: Failed to load mo-file for translation: " + moFile)

    # Hack alert:
    #
    # The following special-case is necessary for Ubuntu, since their
    # translations are shipped in a single huge package. The downside to
    # this special case, aside from the simple fact that there is one,
    # is that it makes automatic translations much slower.

    from dogtail import distro
    language = os.environ.get('LANGUAGE', os.environ['LANG'])[0:2]
    if isinstance(distro.distro, distro.Ubuntu):
        load('language-pack-gnome-%s' % language, language)
    load(packageName, language, getDependencies)
