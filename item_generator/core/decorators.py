# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '28 May 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from functools import wraps


def accepts_preprocessors(func):
    """
    Allows preprocessors to work on the input arguments

    Args:
        filepath
    Kwargs
        source_media
        **kwargs

    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        pre_processors = kwargs.get('pre_processors', [])

        # Remove the reference to self
        self = args[0]
        args = args[1:]

        for pprocessor in pre_processors:
            # Modify the input arguments
            args, kwargs = pprocessor.run(*args, **kwargs)

        response = func(self, *args, **kwargs)
        return response
    return wrapper


def accepts_postprocessors(func):
    """
    Allows postprocessors to work on the output from the main
    processor. Post processors must accept:

    Args:
        filepath
    Kwargs:
        source_media
        source_dict
        **kwargs

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Call the main processor
        response = func(*args, **kwargs)

        post_processors = kwargs.get('post_processors', [])

        # Remove the reference to self from the first processor.
        args = args[1:]

        for pprocessor in post_processors:

            # Modify the response from the main processor
            response = pprocessor.run(*args, source_dict=response, **kwargs)
        return response

    return wrapper
