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
from .abstract import OperatorBase
from typing import List


@accepts_postprocessors
def header_extract(filepath: str, attributes: List, **kwargs) -> dict:

    engine = plugins.guess_engine()

    # Select the header extraction handler
    backend = plugins.get_backend(engine)

    # Use the handler to extract the desired attributes from the header
    data = backend.extract_attributes(filepath, attributes, **kwargs)

    return data

@accepts_argprocessors
@accepts_postprocessors
def xarray_attr_extraction(
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

    ds = xr.open_dataset(file, **kwargs)

    extracted_metadata = {}
    for attr in attributes:

        value = ds.attrs.get(attr)
        if value:
            extracted_metadata[attr] = value

    return extracted_metadata
