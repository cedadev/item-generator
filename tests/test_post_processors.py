# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '15 Jul 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

import pytest

from item_generator.extraction_methods import postprocessors


@pytest.fixture
def fpath():
    return 'a/b/c/d.txt'


@pytest.fixture
def source_dict():
    return {
        'date': '2021-05-02'
    }


@pytest.fixture
def isodate_processor():
    return postprocessors.ISODateProcessor(date_key='date')


@pytest.fixture
def facet_map_processor():
    return postprocessors.FacetMapProcessor(term_map={'date': 'start_date'})


@pytest.fixture
def bbox_processor():
    return postprocessors.BBOXProcessor(key_list=['west', 'south', 'east', 'north'])


def test_isodate_processor(isodate_processor, fpath, source_dict):
    """Check isodate processor does what's expected"""
    expected = source_dict.copy()
    expected['date'] = '2021-05-02T00:00:00'

    output = isodate_processor.run(fpath, source_dict=source_dict)
    assert output == expected


def test_facet_map_processor(facet_map_processor, fpath, source_dict):
    """
    Check processor changes name of named facets
    """
    expected = {
        'start_date': source_dict['date']
    }

    output = facet_map_processor.run(fpath, source_dict=source_dict)
    assert output == expected


def test_bbox_processor(bbox_processor, fpath):
    source_dict = {
        'north': '42.231201171875',
        'south': '38.5098876953125',
        'east': '-28.706298828125',
        'west': '-37.9745330810547'
    }

    expected = [
        source_dict['west'],
        source_dict['south'],
        source_dict['east'],
        source_dict['north']
    ]

    output = bbox_processor.run(fpath, source_dict=source_dict)
    assert output == expected
