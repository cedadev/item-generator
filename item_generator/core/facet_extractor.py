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

from typing import List, Callable

from item_generator.item_describer import ItemDescriptions
from .utils import ProcessorLoader, dict_merge


class FacetExtractor:

    def __init__(self, conf):
        self.item_description = ItemDescriptions(conf['item_descriptions']['root_directory'])
        self.processors = ProcessorLoader('item_generator.facet_extractors')

    def get_processor(self, name: str) -> Callable:
        """

        :param name: Name of the requested processor
        :return: processor function
        """
        return self.processors.get_processor(name)

    def get_facets(self, filepath: str, source_media: str = 'POSIX', processors: List = []) -> dict:
        """
        Extract the raw facets from the file based on the listed processors

        :param filepath: Path to the file
        :param source_media: The source media type (POSIX, Object, Tape)
        :param processors: List of processing functions to call to extract the facets

        :return: result from the processing
        """
        facets = {}
        for processor in processors:
            processor_name = processor['name']
            processor_inputs = processor.get('inputs', {})
            post_processors = processor.get('post_processors', [])

            loaded_pprocessors = []
            for pprocessor in post_processors:
                pp_name = pprocessor['name']
                loaded_pprocessors.append({
                    'processor': self.get_processor(pp_name),
                    'inputs': pprocessor.get('inputs',{})
                })

            p = self.get_processor(processor_name)

            metadata = p(filepath, source_media=source_media, post_processors=loaded_pprocessors, **processor_inputs)

            facets = dict_merge(facets, metadata)

        return facets

    def process_file(self, filepath, source_media):
        """
        Method to outline the processing pipeline for an individual file
        :param filepath:
        :param source_media:
        :return:
        """

        # Get dataset description file
        description = self.item_description.get_description(filepath)

        # Get default tags
        tags = description.defaults

        # Execute facet extraction functions
        metadata = self.get_facets(filepath, source_media, description.extraction_methods)
        tags.update(metadata)

        print(tags)

        # Process multi-values

        # Apply mappings

        # Apply overrides

        # Convert to URIs

        # Process URIs to human terms

        # Generate item id
        pass