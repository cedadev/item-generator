# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '07 Jun 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

# Package imports
from item_generator.extraction_methods.abstract import BaseProcessor

# 3rd Party Imports

# Python imports
import pkg_resources
import logging

# Typing imports
import collections.abc
from typing import Callable

LOGGER = logging.getLogger(__name__)


class ProcessorLoader:
    def __init__(self, entry_point_key: str):
        """
        Entry points to load from in the setup.py

        :param entry_point_key: name of the entry point source
        """
        self.handlers = {}
        for entry_point in pkg_resources.iter_entry_points(entry_point_key):
            self.handlers[entry_point.name] = entry_point.load()

    def get_processor(self, name: str, **kwargs) -> BaseProcessor:
        """
        Get the processor by name

        :param name: The name of the requested processor

        :return: An callable function
        """
        try:
            return self.handlers[name](**kwargs)
        except KeyError:
            LOGGER.error(f'Failed to load processor: {name}')



def dict_merge(*args, add_keys=True):
    assert len(args) >= 2, "dict_merge requires at least two dicts to merge"

    # Make a copy of the root dict
    rtn_dct = args[0].copy()

    merge_dicts = args[1:]

    for merge_dct in merge_dicts:

        if add_keys is False:
            merge_dct = {key: merge_dct[key] for key in set(rtn_dct).intersection(set(merge_dct))}

        for k, v in merge_dct.items():

            # This is a new key. Add as is.
            if not rtn_dct.get(k):
                rtn_dct[k] = v

            # This is an existing key with mismatched types
            elif k in rtn_dct and type(v) != type(rtn_dct[k]):
                raise TypeError(f"Overlapping keys exist with different types: original is {type(rtn_dct[k])}, new value is {type(v)}")

            # Recursive merge the next level
            elif isinstance(rtn_dct[k], dict) and isinstance(merge_dct[k], collections.abc.Mapping):
                rtn_dct[k] = dict_merge(rtn_dct[k], merge_dct[k], add_keys=add_keys)

            # If the item is a list, append items avoiding duplictes
            elif isinstance(v, list):
                for list_value in v:
                    if list_value not in rtn_dct[k]:
                        rtn_dct[k].append(list_value)
            else:
                rtn_dct[k] = v
    return rtn_dct