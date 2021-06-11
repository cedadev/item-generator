# encoding: utf-8
"""
Collection of functions which can be used to extract metadata from file headers
"""
__author__ = 'Richard Smith'
__date__ = '27 May 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

import cf
from cf import file_type
from item_generator.core.base import BaseBackend
from typing import List


class CfBackend(BaseBackend):
    """
    Cf
    ------

    Backend Name: ``Cf``

    Description:
        Takes an input string and returns a boolean on whether this
        backend can open that file.
    """
    def guess_can_open(self, filepath: str, **kwargs) -> bool:
        try:
            file_type(filepath)
            return True
        except IOError:
            return False

    def attr_extraction(
            self,
            file: str,
            attributes: List,
            **kwargs) -> dict:
        """
        Takes a filepath and list of attributes and extracts the metadata.

        :param file: file-like object
        :param attributes: attributes to extract
        :param kwargs: kwargs to send to cf.read().

        :return: Dictionary of extracted attributes
        """

        ds = cf.read(file, **kwargs)

        extracted_metadata = {}
        for attr in attributes:

            value = ds.attrs.get(attr)
            if value:
                extracted_metadata[attr] = value

        return extracted_metadata
