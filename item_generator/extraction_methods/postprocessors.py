# encoding: utf-8
"""
Post processors operate on the output from a main processor.
They are used using the same interface as a main processor ``process``
but they accept the result of the previous step as part of the ``process`` signature.
"""
__author__ = 'Richard Smith'
__date__ = '28 May 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

import logging
# Python imports
from abc import abstractmethod

# Package imports
from asset_scanner.core.processor import BaseProcessor
# 3rd Party imports
from dateutil.parser import ParserError, parse

LOGGER = logging.getLogger(__name__)


class BasePostProcessor(BaseProcessor):

    @abstractmethod
    def run(self, filepath: str, source_media: str = 'POSIX', source_dict: dict = {}, **kwargs) -> dict:
        pass


class FacetMapProcessor(BasePostProcessor):
    """

    Processor Name: ``facet_map``

    Description:
        In some cases, you may wish to map the header attributes to different
        facets. This method takes a map and converts the facet labels into those
        specified.

    Configuration Options:
        ``term_map``: Dictionary of terms to map

    Example Configuration:

    .. code-block:: yaml

        post_processors:
            - name: facet_map
              inputs:
                term_map:
                    time_coverage_start: start_time

    """

    def run(self, filepath: str, source_media: str = 'POSIX', source_dict: dict = {}, **kwargs ):
        output = {}

        for k, v in source_dict.items():

            new_key = self.term_map.get(k)
            if new_key:
                output[new_key] = v
            else:
                output[k] = v

        return output


class ISODateProcessor(BasePostProcessor):
    """
    ISO 8601 Date Processor
    -----------------------

    Processor Name: ``isodate_processor``

    Description:
        Takes the source dict and the key to access the date and
        converts the date to ISO 8601 Format.

        e.g.

        ``YYYY-MM-DDTHH:MM:SS.ffffff``, if microsecond is not 0
        ``YYYY-MM-DDTHH:MM:SS``, if microsecond is 0

        If the date format cannot be parsed, it is removed from the source dict with
        an error logged.

    Configuration Options:
        ``date_key``: name of the key to the date value

    Example Configuration:

        .. code-block:: yaml

            post_processors:
                - name: isodate_processor
                  inputs:
                    date_key: time

    """

    def run(self, filepath: str, source_media: str = 'POSIX', source_dict={}, **kwargs) -> dict:
        """
        :param filepath: file currently being processed
        :param source_media: media source of the file being processed
        :param source_dict: dict containing the date value

        :return: the source dict with the date converted to ISO8601 format.
        """
        if source_dict.get(self.date_key):
            date = source_dict[self.date_key]

            try:
                date = parse(date).isoformat()
                source_dict[self.date_key] = date
            except ValueError as e:
                LOGGER.error(f'Error parsing date from file: {filepath} on media: {source_media} - {e}')

                # remove the bad date from the dict
                source_dict.pop(self.date_key)
        else:
            # Clean up empty strings and non-matches
            source_dict.pop(self.date_key, None)

        return source_dict


class BBOXProcessor(BasePostProcessor):
    """

    Processor Name: ``stac_bbox``

    Description:
        Accepts a dictionary of coordinate values and converts to `RFC 7946, section 5 <https://tools.ietf.org/html/rfc7946#section-5>`_
        formatted bbox.

    Configuration Options:
        ``key_list``: ``REQUIRED`` list of keys to convert to bbox array. Ordering is respected.

    Example Configuration:

    .. code-block:: yaml

        post_processors:
            - name: stac_bbox
              inputs:
                key_list:
                   - west
                   - south
                   - east
                   - north

    """

    def run(self, filepath: str, source_media: str = 'POSIX', source_dict: dict = {}, **kwargs ):

        try:
            rfc_bbox = [float(source_dict[key]) for key in self.key_list]
            source_dict = rfc_bbox
        except KeyError:
            LOGGER.warning(f'Unable to convert bbox.', exc_info=True)

        return source_dict


class StringJoinProcessor(BasePostProcessor):
    """

    Processor Name: ``string_join``

    Description:
        Accepts a dictionary. String values are popped from the dictionary and
        are put back into the dictionary with the ``output_key`` specified.

    Configuration Options:
        ``key_list``: ``REQUIRED`` list of keys to convert to bbox array. Ordering is respected.
        ``delimiter``: ``REQUIRED`` text delimiter to put between strings
        ``output_key``: ``REQUIRED`` name of the key you would like to output

    Example Configuration:

    .. code-block:: yaml

        post_processors:
            - name: string_join
              inputs:
                key_list:
                   - year
                   - month
                   - day
                delimiter: -
                output_key: datetime

    """

    def run(self, filepath: str, source_media: str = 'POSIX', source_dict: dict = {}, **kwargs ):

        try:
            string_elements = [str(source_dict.pop(key)) for key in self.key_list]
            source_dict[self.output_key] = self.delimiter.join(string_elements)
        except KeyError:
            LOGGER.warning(f'Unable merge strings. file: {filepath}', exc_info=True)

        return source_dict