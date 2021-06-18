# encoding: utf-8
"""
"""
__author__ = 'Richard Smith'
__date__ = '27 May 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

# Package imports
from item_generator.core.decorators import accepts_postprocessors
from asset_scanner.core.processor import BaseProcessor

# 3rd Party imports

# Python imports
import re
import os


class RegexExtract(BaseProcessor):
    """
    Regex
    ------

    Processor Name: ``regex``
    Accepts Post-Processors: yes


    Description:
        Takes an input string and a regex with
        named capture groups and returns a dictionary of the values
        extracted using the named capture groups.

    Configuration Options:
        `regex`: The regular expression to match against the filepath
    """

    @accepts_postprocessors
    def run(self, filepath: str, source_media: str ='POSIX', **kwargs) -> dict:

        m = re.match(self.regex, filepath)

        if m:
            return m.groupdict()

        return {}


class FilenameRegexExtract(RegexExtract):
    """
    Filename Regex
    --------------

    Processor Name: ``filename_regex``
    Accepts Post-Processors: yes


    Description:
        Takes an input string and a regex with
        named capture groups and returns a dictionary of the values
        extracted using the named capture groups.

        This turns the filepath into just the basename as output by
        ``os.path.basename``

    Configuration Options:
        `regex`: The regular expression to match against the filepath
    """

    @accepts_postprocessors
    def run(self, filepath: str, source_media: str = 'POSIX', **kwargs) -> dict:

        filepath = os.path.basename(filepath)

        return super().run(filepath, source_media, **kwargs)
