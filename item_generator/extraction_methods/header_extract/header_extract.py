# encoding: utf-8
"""
Collection of functions which can be used to extract metadata from file headers
"""
__author__ = 'Richard Smith'
__date__ = '27 May 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

import xarray as xr
import pkg_resources as pkg
from item_generator.core.base import BaseProcessor, BaseBackend
from item_generator.core.decorators import accepts_postprocessors, accepts_argprocessors
from typing import List
from collections.abc import Sequence


class HeaderExtract(BaseProcessor):
    """
    Header
    ------

    Processor Name: ``header``
    Accepts Post-Processors: yes


    Description:
        Takes an input string and a regex with
        named capture groups and returns a dictionary of the values
        extracted using the named capture groups.

    Configuration Options:
        `header`: The regular expression to match against the filepath
    """
    @accepts_postprocessors
    def process(self, filepath: str, attributes: List, **kwargs) -> dict:

        backend = self.guess_backend(filepath)

        # Use the handler to extract the desired attributes from the header
        data = self.attr_extraction(backend, filepath, attributes, **kwargs)

        return data
    
    def list_backend(self):
        return pkg.iter_entry_points("item_generator.extraction_methods.header_extract.backends")
    
    def guess_backend(self, filepath: str, **kwargs) -> dict:
        backends = self.list_backend()

        for backend in backends:
            if backend.guess_can_open(filepath):
                return backend

        raise ValueError(
            f"Could not find backend to open file: {filepath}"
        )
    
    @accepts_argprocessors
    @accepts_postprocessors
    def attr_extraction(
            backend: Sequence(BaseBackend),
            file: str,
            attributes: List,
            argprocessors: List = ['posix_file'],
            postprocessors: List = [],
            **kwargs) -> dict:
        """
        Takes a filepath and list of attributes and extracts the metadata from the header.

        :param file: file-like object
        :param attributes: Header attributes to extract
        :param argprocessors: list of processors to modify the arguments before being
        put into this function
        :param postprocessors: can be used to modify the output
        :param kwargs: kwargs to send to xarray.open_dataset(). e.g. engine to
        specify different engines to use with grib data.

        :return: Dictionary of extracted attributes
        """

        return backend.attr_extraction(file, attributes, **kwargs)
