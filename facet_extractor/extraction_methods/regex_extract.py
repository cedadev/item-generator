# encoding: utf-8
"""
Regular expression based facet extraction functions
"""
__author__ = 'Richard Smith'
__date__ = '27 May 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

import re


def string_regex(input_string: str, regex: str) -> dict:
    """
    Takes an input string (like a filepath) and a regex with
    named capture groups and returns a dictionary of the values
    extracted using the named capture groups.

    :param input_string: string to match against
    :param regex: pattern to match

    :return: Dictionary of the values from the named capture groups
    """

    m = re.match(regex, input_string)

    if m:
        return m.groupdict()
    return {}