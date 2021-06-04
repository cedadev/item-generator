# encoding: utf-8
"""


Configuration
-------------

.. code-block:: yaml

    item_descriptions:
        root_directory: /path/to/root/descriptions

"""
__author__ = 'Richard Smith'
__date__ = '27 May 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from typing import List

from item_generator.item_describer import ItemDescriptions


class FacetExtractor:

    def __init__(self, conf):
        self.item_description = ItemDescriptions(conf['item_descriptions']['root_directory'])

    def get_processor(self):
        pass

    def get_facets(self, filepath: str, source_media: str = 'POSIX', processors: List = []) -> dict:
        """
        Extract the raw facets from the file based on the listed processors

        :param filepath: Path to the file
        :param source_media: The source media type (POSIX, Object, Tape)
        :param processors: List of processing functions to call to extract the facets

        :return: result from the processing
        """
        for processor in processors:

        pass

    def process_file(self, filepath, source_media):
        """
        Method to outline the processing pipeline for an individual file
        :param filepath:
        :param source_media:
        :return:
        """

        # Get dataset description file
        description = self.item_description.get_description(filepath)
        print(description)

        # Get default tags
        tags = description.defaults
        print(tags)

        # Execute facet extraction functions
        metadata = self.get_facets(filepath, source_media, description.extraction_methods)

        # Process multi-values

        # Apply mappings

        # Apply overrides

        # Convert to URIs

        # Process URIs to human terms

        # Generate item id
        pass