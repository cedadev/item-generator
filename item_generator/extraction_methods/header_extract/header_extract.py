# encoding: utf-8
"""
Collection of functions which can be used to extract metadata from file headers
"""
__author__ = 'Richard Smith'
__date__ = '27 May 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

import logging
from typing import List

import pkg_resources as pkg
from asset_scanner.core.processor import BaseProcessor

from item_generator.core.decorators import accepts_postprocessors

LOGGER = logging.getLogger(__name__)


class HeaderExtract(BaseProcessor):
    """

    .. list-table::

        * - Processor Name
          - ``header_extract``
        * - Accepts Pre-processors
          - .. fa:: times
        * - Accepts Post-processors
          - .. fa:: check

    Description:
        Takes a filepath string and a list of attributes
        and returns a dictionary of the values extracted from the 
        file header.

    Configuration Options:
        - ``attributes``: A list of attributes to match agains the filePath
        - ``post_processors``: List of post_processors to apply

    Example configuration:
        .. code-block:: yaml

            - name: header_extract
              inputs:
                attributes:
                    - institution
                    - sensor
                    - platform


    """
    @accepts_postprocessors
    def run(self, filepath: str, attributes: List, **kwargs) -> dict:

        backend = self.guess_backend(filepath)

        # Use the handler to extract the desired attributes from the header
        data = self.attr_extraction(backend, filepath, attributes, **kwargs)

        return data
    
    def list_backend(self):
        backend_entrypoints = {}
        for pkg_ep in pkg.iter_entry_points("item_generator.extraction_methods.header_extract.backends"):
            name = pkg_ep.name
            try:
                backend = pkg_ep.load()
                backend_entrypoints[name] = backend
            except Exception as ex:
                LOGGER(ex)
        return backend_entrypoints
    
    def guess_backend(self, filepath: str, **kwargs) -> dict:
        backends = self.list_backend()
        for engine, backend in backends.items():
            backend = backend()
            if backend.guess_can_open(filepath):
                return backend
        
        raise(f"No backend found for file {filepath}")
        


    @accepts_postprocessors
    def attr_extraction(
            self,
            backend,
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
