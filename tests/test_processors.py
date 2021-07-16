# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '15 Jul 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

import pytest

from item_generator.extraction_methods.regex_extract import RegexExtract
from item_generator.extraction_methods.header_extract import HeaderExtract

@pytest.fixture
def regex_processor():
    return RegexExtract(
        regex=r'^(?:\w*[\s]){2}(?P<interesting>\w*)'
    )


def test_regex_extract(regex_processor):
    """Check can extract groups with regex"""

    input = 'this contains interesting stuff'
    expected = {
        'interesting': 'interesting'
    }

    output = regex_processor.run(input)
    assert output == expected