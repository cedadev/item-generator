# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '07 Jun 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from abc import ABC, abstractmethod
from typing import List


class BaseProcessor(ABC):
    """
    Class to act as a base for all processors. Defines the basic method signature
    and ensure compliance by all subclasses.
    """

    def __init__(self, **kwargs):
        """
        Set the kwargs to generate instance attributes of the same name
        :param kwargs:
        """

        for k, v in kwargs.items():
            setattr(self, k, v)

    @abstractmethod
    def process(self, filepath: str, media_source: str = 'POSIX', **kwargs) -> dict:
        """
        The action of running the processor and returning an output
        :param filepath: Path to object
        :param media_source: Media type for the target object
        :param kwargs: free kwargs passed to the processor.
        :return: dict
        """
        pass


class BaseBackend(ABC):
    """
    Class to act as a base for all backends. Defines the basic method signature
    and ensure compliance by all subclasses.
    """

    def __init__(self, **kwargs):
        """
        Set the kwargs to generate instance attributes of the same name
        :param kwargs:
        """

        for k, v in kwargs.items():
            setattr(self, k, v)

    @abstractmethod
    def guess_can_open(self, filepath: str, **kwargs) -> bool:
        """
        Check if backend can open file
        :param filepath: Path to object
        :param kwargs: free kwargs passed to the check.
        :return: bool
        """
        pass
    
    @abstractmethod
    def attr_extraction(
            self,
            file: str,
            attributes: List,
            **kwargs) -> dict:
        """
        Takes a filepath and list of attributes and extracts the metadata.

        :param file: file-like object
        :param attributes: attributes to extract
        :param kwargs: kwargs to send to xarray.open_dataset(). e.g. engine to
        specify different engines to use with grib data.

        :return: Dictionary of extracted attributes
        """
        pass
