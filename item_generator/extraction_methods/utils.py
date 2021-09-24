# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '03 Jun 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

import re
from typing import Any
from string import Template

from asset_scanner.core.utils import generate_id


DATE_TEMPLATE = Template('${year}-${month}-${day}T${hour}:${minute}:${second}')


def is_remote_uri(path: str) -> bool:
    """Finds URLs of the form protocol:// or protocol::
    This also matches for http[s]://, which were the only remote URLs
    supported in <=v0.16.2.
    """
    return bool(re.search(r"^[a-z][a-z0-9]*(\://|\:\:)", path))


def generate_item_id_from_properties(filepath, tags, description):

    has_all_facets = all([facet in tags for facet in description.aggregation_facets])

    if has_all_facets:
        id_string = ''
        for facet in description.aggregation_facets:
            vals = tags.get(facet)
            if isinstance(vals, (str, int)):
                id_string = '.'.join((id_string, vals))
            if isinstance(vals, (list)):
                id_string = '.'.join((id_string, f'multi_{facet}'))

        return generate_id(id_string)

    return generate_id(filepath)