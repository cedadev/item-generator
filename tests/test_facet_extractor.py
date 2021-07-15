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

PROCESSORS = [
    'regex',
    'header_extract'
]

PRE_PROCESSORS = [
    'filename_reducer'
]

POST_PROCESSORS = [
    'isodate_processor',
    'facet_map'
]


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
    """Initialise facet extractor"""
    return FacetExtractor(extractor_conf)


def test_can_load_processors(extractor):
    """
    Check we have loaded all processors we expect to load
    """
    for processor in PROCESSORS:
        assert extractor._get_processor(processor)


def test_can_load_pre_processors(extractor):
    """
    Check we have loaded all pre-processors we expect to load
    """
    for processor in PRE_PROCESSORS:
        assert extractor._get_processor(processor, 'pre_processors')


def test_can_load_post_processors(extractor):
    """
    Check we have loaded all post processors we expect to load
    """
    for processor in POST_PROCESSORS:
        assert extractor._get_processor(processor, 'post_processors')


def test__load_processor(extractor):
    """
    Check can load processors
    """
    processor = {
        'name': 'regex'
    }

    p = extractor._load_processor(processor)
    assert p.__class__.__name__ == 'RegexExtract'


def test__load_extra_processors(extractor):
    """
    Check can load extra processors
    """
    processor = {
        'name': 'regex',
        'post_processors': [
            {
                'name': 'isodate_processor',
                'date_key': 'date'
            }
        ]
    }

    ps = extractor._load_extra_processors(processor, 'post_processors')
    assert len(ps) == 1
    assert ps[0].__class__.__name__ == 'ISODateProcessor'
