# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '28 May 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'


def facet_map(source_dict: dict, term_map: dict) -> dict:
    """
    In some cases, you may wish to map the header attributes to different
    facets. This method takes a map and converts the facet labels into those
    specified.

    :param source_dict: source_dict for modification
    :param term_map: map to modify source dict keys

    :returns: dict with keys remapped
    """

    output = {}

    for k,v in source_dict.items():

        new_key = term_map.get(k)
        if new_key:
            output[new_key] = v
        else:
            output[k] = v

    return output
