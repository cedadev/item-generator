# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '15 Jul 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

import pytest
import os
from unittest import TestCase
import ast

from item_generator import FacetExtractor

PROCESSORS = [
    'regex',
    'header_extract',
    'iso19115'
]

PRE_PROCESSORS = [
    'filename_reducer',
    'ceda_observation'
]

POST_PROCESSORS = [
    'isodate_processor',
    'facet_map',
    'stac_bbox'
]


@pytest.fixture
def data_path():
    mod_path = os.path.realpath(__file__)
    test_path = os.path.dirname(mod_path)
    return os.path.join(test_path, 'data')


@pytest.fixture
def extractor_conf(data_path):
    return {
        "extractor": "item_generator.FacetExtractor",
        "item_descriptions": {
            "root_directory": os.path.join(data_path, 'descriptions'),
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
                'date_keys': ['date']
            }
        ]
    }

    ps = extractor._load_extra_processors(processor, 'post_processors')
    assert len(ps) == 1
    assert ps[0].__class__.__name__ == 'ISODateProcessor'


def test_run_processors(extractor):
    """
    Check run_processors method for errors
    """
    path = '/badc/faam/data/2005/b069-jan-05/core_processed/core_faam_20050105_r0_b069.nc'
    description = extractor.item_descriptions.get_description(path)

    expected = {'properties': {'datetime': '2005-01-05T00:00:00', 'platform': 'faam', 'flight_number': 'b069'}}

    output = extractor.run_processors(
        path,
        description
    )

    assert output == expected


def test_process_file(extractor, capsys):
    """
    Check the process_file method. As this method does not return a value,
    need to capture the stdout and test against that.
    """
    path = '/badc/faam/data/2005/b069-jan-05/core_processed/core_faam_20050105_r0_b069.nc'
    expected_facet = {
        'id': 'e51bff4c0c383366fcb422983f5b1de3',
        'body': {
            'item_id': 'e51bff4c0c383366fcb422983f5b1de3',
            'type': 'item',
            'properties': {
                'datetime': '2005-01-05T00:00:00',
                'platform': 'faam',
                'flight_number': 'b069'
            }
        }
    }

    expected_asset = {'id': '3b65eee251f13679d90ca569061dd407',
                      'body': {'collection_id': 'e51bff4c0c383366fcb422983f5b1de3'}}

    extractor.process_file(path, 'POSIX')

    # Parse the stdout to retrive the output
    captured = capsys.readouterr()
    facets, assets = captured.out.strip().split('\n')

    # Can't use JSON.loads() as string in format "{'key':'value'}"
    facets = ast.literal_eval(facets)
    assets = ast.literal_eval(assets)

    TestCase().assertDictEqual(expected_facet, facets)
    TestCase().assertDictEqual(expected_asset, assets)
