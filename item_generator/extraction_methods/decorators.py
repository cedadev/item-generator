# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '28 May 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from functools import wraps


def accepts_argprocessors(func):
    """
    Uses the arg processors to modify the function
    arguments before being passed into the operation.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):

        argprocessors = kwargs.get('argprocessors', [])

        # Run any preprocessors
        for processor in argprocessors:
            args, kwargs = processor.run(*args, **kwargs)

        func(*args, **kwargs)

        # Clean up after processors
        for processor in preprocessors:
            args, kwargs = processor.cleanup(*args, **kwargs)

    return wrapper


def accepts_postprocessors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
    return wrapper


