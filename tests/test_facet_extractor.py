# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '15 Jul 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

import ast
import os
import pytest
from pathlib import Path
from unittest import TestCase

from asset_scanner.core.utils import generate_id
from asset_scanner.core.item_describer import ItemDescriptions
from asset_scanner.types.source_media import StorageType

from item_generator import FacetExtractor


PROCESSORS = [
    'regex',
    'header_extract',
    'iso19115',
    'xml_extract',
]

PRE_PROCESSORS = [
    'filename_reducer',
    'ceda_observation',
]

POST_PROCESSORS = [
    'isodate_processor',
    'facet_map',
    'stac_bbox',
    'string_join',
    'date_combinator',
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
        assert extractor._get_processor(processor, 'facet_processors')


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

    p = extractor._load_facet_processor(processor)
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


@pytest.mark.xfail(reason='approach has changed, needs fixing.')
def test_process_file(extractor, capsys):
    """
    Check the process_file method. As this method does not return a value,
    need to capture the stdout and test against that.
    """
    path = '/badc/faam/data/2005/b069-jan-05/core_processed/core_faam_20050105_r0_b069.nc'
    expected_facet = {
        'id': 'c9ba1eb86ad1599bc715791e9f5af9de',
        'body': {
            'item_id': 'c9ba1eb86ad1599bc715791e9f5af9de',
            'collection_id': '5e543256c480ac577d30f76f9120eb74',
            'type': 'item',
            'properties': {
                'datetime': '2005-01-05T00:00:00',
                'platform': 'faam',
                'flight_number': 'b069'
            }
        }
    }

    expected_asset = {'id': '3b65eee251f13679d90ca569061dd407',
                      'body': {'item_id': 'c9ba1eb86ad1599bc715791e9f5af9de'}}

    extractor.process_file(path, 'POSIX')

    # Parse the stdout to retrive the output
    captured = capsys.readouterr()
    facets, assets = captured.out.strip().split('\n')

    # Can't use JSON.loads() as string in format "{'key':'value'}"
    facets = ast.literal_eval(facets)
    assets = ast.literal_eval(assets)

    TestCase().assertDictEqual(expected_facet, facets)
    TestCase().assertDictEqual(expected_asset, assets)


def test_collection_id_undefined(extractor):
    """Test when no id section is present.

    This should return MD5 hash of undefined
    """

    filepath = '/badc/faam/data/2005/b069-jan-05/core_processed/core_faam_20050105_r0_b069.nc'
    expected = generate_id('undefined')

    description = extractor.item_descriptions.get_description(filepath)
    id = extractor.get_collection_id(description, filepath, StorageType.POSIX)

    assert id == expected


def test_collection_id_default(extractor, data_path):
    """Test when no id section is present with default and no processor.

    This should return MD5 hash of default
    """

    # Specify item description
    file_list = [os.path.join(
        data_path,
        'collection_descriptions',
        'faam_default_collection_id.yml'
    )]

    file_list = [Path(file) for file in file_list]

    item_description = ItemDescriptions(
        filelist=file_list
    )

    # Replace item descriptions object
    extractor.item_descriptions = item_description

    filepath = '/badc/faam/data/2005/b069-jan-05/core_processed/core_faam_20050105_r0_b069.nc'
    expected = generate_id('undefined')

    description = extractor.item_descriptions.get_description(filepath)
    id = extractor.get_collection_id(description, filepath, StorageType.POSIX)
    print(id)

    assert id == expected


def test_collection_id_generated(extractor, data_path):
    """Test when no id section is present with processor.

    This should return MD5 hash of `faam`
    """

    # Specify item description to load
    file_list = [os.path.join(
        data_path,
        'collection_descriptions',
        'faam_generated_collection_id.yml'
    )]

    file_list = [Path(file) for file in file_list]

    item_description = ItemDescriptions(
        filelist=file_list
    )

    # Replace item descriptions object
    extractor.item_descriptions = item_description

    filepath = '/badc/faam/data/2005/b069-jan-05/core_processed/core_faam_20050105_r0_b069.nc'
    expected = generate_id('faam')

    description = extractor.item_descriptions.get_description(filepath)
    id = extractor.get_collection_id(description, filepath, StorageType.POSIX)

    assert id == expected


@pytest.mark.xfail(reason='approach has changed, needs fixing.')
def test_templating(extractor, capsys):
    """
       Check the process_file method. As this method does not return a value,
       need to capture the stdout and test against that. Check that the template
       engine works as expected.
       """
    path = '/badc/spam/data/2005/b069-jan-05/core_processed/core_faam_20050105_r0_b069.nc'
    expected_title = 'spam flight no. b069'
    expected_description = 'Data recorded as part of the spam project during flight number b069 which took place on 2005-01-05T00:00:00.'

    extractor.process_file(path, 'POSIX')

    # Parse the stdout to retrive the output
    captured = capsys.readouterr()
    facets, assets = captured.out.strip().split('\n')

    # Can't use JSON.loads() as string in format "{'key':'value'}"
    facets = ast.literal_eval(facets)
    assets = ast.literal_eval(assets)

    assert facets['body']['properties']['title'] == expected_title
    assert facets['body']['properties']['description'] == expected_description