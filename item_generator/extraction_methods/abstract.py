# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '28 May 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from abc import ABC
from typing import Union, IO


class OperatorBase(ABC):

    @abstractmethod
    def guess_can_operate(self, filename_or_obj: Union[str, IO]) -> bool:
        """
        Method to test if the supplied method applies to the file or
        object type

        :param filename_or_obj:
        :return:
        """
        return False

    @abstractmethod
    def operate(self, filename_or_obj, **kwargs):
        """

        :param filename_or_obj:
        :param kwargs:
        :return:
        """
