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

from asset_scanner.core import BaseExtractor
from asset_scanner.core.utils import dict_merge, generate_id
from asset_scanner.core.processor import BaseProcessor
from asset_scanner.core.item_describer import ItemDescriptions, ItemDescription

import logging

LOGGER = logging.getLogger(__name__)

from typing import List, Callable


class FacetExtractor(BaseExtractor):
    PROCESSOR_ENTRY_POINT = 'item_generator.facet_extractors'

    def _load_extra_processors(self, processor: dict, key: str) -> List[BaseProcessor]:
        """
        Load the post processors for the given processor

        :param processor: Configuration for the processor including any post processor
        :param key: The name of the key which holds the list of extra processors

        :return: List of loaded processors.
        """

        loaded_pprocessors = []

        for pprocessor in processor.get(key, []):
            pp_name = pprocessor['name']
            pp_kwargs = pprocessor.get('inputs', {})

            loaded = self._get_processor(pp_name, **pp_kwargs)

            if loaded:
                loaded_pprocessors.append(loaded)

        return loaded_pprocessors

    def _load_processor(self, processor: dict) -> BaseProcessor:
        processor_name = processor['name']
        processor_inputs = processor.get('inputs', {})

        return self._get_processor(processor_name, **processor_inputs)

    def _get_processor(self, name: str, **kwargs) -> BaseProcessor:
        """

        :param name: Name of the requested processor
        :return: processor object
        """
        return self.processors.get_processor(name, **kwargs)

    @staticmethod
    def _generate_item_id(filepath, tags, description):

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

    def get_facets(self, filepath: str, description: ItemDescription, source_media: str = 'POSIX', ) -> dict:
        """
        Extract the raw facets from the file based on the listed processors

        :param filepath: Path to the file
        :param source_media: The source media type (POSIX, Object, Tape)
        :param processors: List of processing functions to call to extract the facets

        :return: result from the processing
        """
        # Get default tags
        tags = description.defaults

        # Execute facet extraction functions
        processors = description.extraction_methods

        for processor in processors:
            # Load the processors
            p = self._load_processor(processor)
            pre_processors = self._load_extra_processors(processor, 'pre_processors')
            post_processors = self._load_extra_processors(processor, 'post_processors')


            # Retrieve the metadata
            metadata = p.run(filepath, source_media=source_media, post_processors=post_processors, pre_processors=pre_processors)

            # Merge the extracted metadata with the metadata already retrieved
            tags = dict_merge(tags, metadata)

        # Process multi-values

        # Apply mappings

        # Apply overrides

        # Convert to URIs

        # Process URIs to human terms

        return tags

    def process_file(self, filepath, source_media):
        """
        Method to outline the processing pipeline for an individual file
        :param filepath:
        :param source_media:
        :return:
        """
        LOGGER.info(f'Processing: {filepath}')

        # Get dataset description file
        description = self.item_descriptions.get_description(filepath)

        # TODO: This section should return a dict for merging. Allows processors to add
        # metadata outside the properties section. Can use the dict merge function for
        # deep dictionary merging.
        tags = self.get_facets(filepath, description, source_media)

        # Generate item id
        id = self._generate_item_id(filepath, tags, description)

        output = {
            'id': id,
            'body': {
                'item_id': id,
                'type': 'item',
                'properties': tags
            }
        }

        # Output the item
        self.output(output, namespace='facets')

        # Add item id to asset
        output = {
            'id': generate_id(filepath),
            'body': {
                'collection_id': id
            }
        }
        self.output(output, namespace='assets')
