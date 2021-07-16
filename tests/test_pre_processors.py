# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '15 Jul 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

import pytest

from item_generator.extraction_methods.preprocessors import ReducePathtoName


@pytest.fixture
def filename_reducer():
    """
    Create filename_reducer instance
    :return:
    """
    return ReducePathtoName()


def test_filename_reducer_posix(filename_reducer):
    """
    Check that pre-processor extracts the filename from the POSIX path
    :param filename_reducer:
    :return:
    """
    input = '/a/b/c/d.txt'
    expected = 'd.txt'

    args, kwargs = filename_reducer.run(input)
    assert args[0] == expected
