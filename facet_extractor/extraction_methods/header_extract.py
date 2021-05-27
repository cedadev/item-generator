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


def xarray_header_extraction(path: str, attributes, preprocessor: str ='posix_file', **kwargs) -> dict:
    """

    :param path: File path:
    :param attributes: Header attributes to extract
    :param preprocessor: provides a file-like object to the xarray.Dataset
    :param kwargs: kwargs to send to xarray.Dataset.
    :return: Dictionary of extracted attributes
    """

    pass
