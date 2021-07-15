# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '15 Jul 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

import pytest

from item_generator import FacetExtractor


@pytest.fixture
def extractor_conf(tmp_path):
    return {
        "extractor": "item_generator.FacetExtractor",
        "item_descriptions": {
            "root_directory": tmp_path
        },
        "inputs": [
            {
                "name": "file_system",
                "path": "/badc/faam/data/2005/b069-jan-05"
            }
        ],
        "outputs": [
            {
                "name": "standard_out"
            }
        ]
    }


@pytest.fixture
def extractor(extractor_conf):
    return FacetExtractor(extractor_conf)


def test_loaded_processors(extractor):
    assert 'regex' in extractor.processors.handlers
    assert 'filename_reducer' in extractor.pre_processors.handlers
    assert 'isodate_processor' in extractor.post_processors.handlers


def test__get_processor(extractor):
    processor = extractor._get_processor('regex')
    assert processor.__class__.__name__ == 'RegexExtract'

    processor = extractor._get_processor('isodate_processor', 'post_processors')
    assert processor.__class__.__name__ == 'ISODateProcessor'

    processor = extractor._get_processor('filename_reducer', 'pre_processors')
    assert processor.__class__.__name__ == 'ReducePathtoName'
