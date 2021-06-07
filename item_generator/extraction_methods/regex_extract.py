# encoding: utf-8
"""
Regex
-----

Processor name: ``regex``

Regular expression based facet extraction function

"""
__author__ = 'Richard Smith'
__date__ = '27 May 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

import re
from .decorators import accepts_postprocessors


@accepts_postprocessors
def regex_extract(filepath: str, source_media: str = 'POSIX', regex: str = '', **kwargs) -> dict:
    """
    Takes an input string and a regex with
    named capture groups and returns a dictionary of the values
    extracted using the named capture groups.

    :param filepath: string to match against
    :param source_media: Source media of the file
    :param regex: regex pattern with named capture groups
    :param kwargs:

    :return: extracted groups
    """

    m = re.match(regex, filepath)

    if m:
        return m.groupdict()

    return {}
