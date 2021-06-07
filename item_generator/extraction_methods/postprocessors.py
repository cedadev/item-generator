# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '28 May 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from dateutil.parser import parse
from dateutil.parser import ParserError
import logging

LOGGER = logging.getLogger(__name__)


def facet_map(filepath, source_media, source_dict: dict, term_map: dict) -> dict:
    """
    In some cases, you may wish to map the header attributes to different
    facets. This method takes a map and converts the facet labels into those
    specified.

    :param source_dict: source_dict for modification
    :param term_map: map to modify source dict keys

    :returns: dict with keys remapped
    """

    output = {}

    for k,v in source_dict.items():

        new_key = term_map.get(k)
        if new_key:
            output[new_key] = v
        else:
            output[k] = v

    return output


def date_convert(filepath, source_media, source_dict: dict, date_key: str) -> dict:
    """
    Takes the source dict and the key to access the date and
    converts the date to ISO 8601 Format.

    e.g.

    YYYY-MM-DDTHH:MM:SS.ffffff, if microsecond is not 0
    YYYY-MM-DDTHH:MM:SS, if microsecond is 0

    If the date format cannot be parsed, it is removed from the source dict with
    an error logged.

    :param filepath: file currently being processed
    :param source_media: media source of the file being processed
    :param source_dict: dict containing the date value
    :param date_key: name of the key to the date value

    :return: the source dict with the date converted to ISO8601 format.
    """

    if source_dict.get(date_key):
        date = source_dict[date_key]

        try:
            date = parse(date).isoformat()
            source_dict[date_key] = date
        except ValueError as e:
            LOGGER.error(f'Error parsing date from file: {filepath} on media: {source_media} - {e}')

            # remove the bad date from the dict
            source_dict.pop(date_key)


    return source_dict