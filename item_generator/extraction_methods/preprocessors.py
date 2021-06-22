# encoding: utf-8
"""
Pre-Processors
---------------

Pre processors operate on the input arguments for the main processor.

They can be used to manipuate the input arguments for a given processor to
modify its behaviour.
"""
__author__ = 'Richard Smith'
__date__ = '11 Jun 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

# Package imports
from asset_scanner.core.processor import BaseProcessor
import abc

import os

class BasePreProcessor(BaseProcessor):

    @abc.abstractmethod
    def run(self, filepath: str, source_media: str = 'POSIX', **kwargs) -> dict:
        pass


class ReducePathtoName(BasePreProcessor):
    """
    Filename Reducer
    ----------------

    Processor Name: `filename_reducer`

    Takes a file path and returns the filename using `os.path.basename`.

    """

    def run(self, filepath: str, source_media: str = 'POSIX', **kwargs):

        filepath = os.path.basename(filepath)

        return (filepath, source_media), kwargs

