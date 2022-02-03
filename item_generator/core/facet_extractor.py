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

import logging

from asset_scanner.core import BaseExtractor
from asset_scanner.core.item_describer import ItemDescription, ItemDescriptions
from asset_scanner.core.processor import BaseProcessor
from asset_scanner.core.utils import dict_merge, dot2dict, generate_id
from asset_scanner.types.source_media import StorageType

from asset_scanner.plugins.extraction_methods import utils as item_utils

from typing import Dict

LOGGER = logging.getLogger(__name__)

from typing import List
from string import Template
from cachetools import LRUCache

class FacetExtractor(BaseExtractor):

    PROCESSOR_ENTRY_POINT = 'item_generator.processors'

    def __init__(self, conf: dict):
        super().__init__(conf)
        self.header_deduplication = conf.get('header_deduplication', False)
        self.collection_id_cache = LRUCache(maxsize=5)

    def get_collection_id(self, description: ItemDescription, filepath: str, storage_media: StorageType) -> str:
        """Return the collection ID for the file."""
        collection_id = getattr(description.collections, 'id', 'undefined')
        return generate_id(collection_id)

    def run_processors(self,
                       filepath: str,
                       description: ItemDescription,
                       source_media: StorageType = StorageType.POSIX,
                       **kwargs: dict) -> dict:
        """
        Extract the raw facets from the file based on the listed processors

        :param filepath: Path to the file
        :param description: ItemDescription
        :param source_media: The source media type (POSIX, Object, Tape)

        :return: result from the processing
        """
        # Get default tags
        tags = description.facets.defaults

        # Execute facet extraction functions
        processors = description.facets.extraction_methods

        for processor in processors:

            metadata = self._run_facet_processor(processor, filepath, source_media)

            # Merge the extracted metadata with the metadata already retrieved
            if metadata:
                tags = dict_merge(tags, metadata)

        # Process multi-values

        # Apply mappings

        # Apply overrides

        # Convert to URIs

        # Process URIs to human terms

        return tags

    def get_sumaries(self, item_id: str, description: 'ItemDescription') -> Dict:

        processor = self._load_processor()

        metadata = processor.run(item_id, description)

        return metadata

    def process_file(self, filepath: str, source_media: str = 'POSIX', **kwargs):
        """
        Method to outline the processing pipeline for an individual file
        :param filepath:
        :param source_media:
        :return:
        """
        # Generate file ID
        file_id = generate_id(filepath)

        LOGGER.info(f'Processing: {filepath}')

        # Get dataset description file
        description = self.item_descriptions.get_description(filepath)

        # Get summaries - aggregated properties from assets.
        summaries = self.get_sumaries(kwargs['item_id'], description)

        processor_output = self.run_processors(filepath, description, source_media, **kwargs)

        properties = processor_output.get('properties', {})

        # Generate title and description properties from templates
        templates = description.facets.templates

        if properties and templates:
            if templates.title:
                title_template = templates.title
                title = Template(title_template).safe_substitute(properties)
                summaries['title'] = title
            if templates.description:
                desc_template = templates.description
                desc = Template(desc_template).safe_substitute(properties)
                summaries['description'] = desc

        # Get collection id
        coll_id = description.collections.id

        # Generate item id
        if kwargs.get('item_id'):
            item_id = kwargs['item_id']
        else:
            item_id = item_utils.generate_item_id_from_properties(
                filepath,
                coll_id,
                properties,
                description
            )

        # Merge properties (facets from the item description) and summaries (facets from elasticsearch aggregations)
        for key, value in properties.items():
            if type(value) == str:
                properties[key] = [value]

        merged_properties = dict_merge(summaries, properties)

        body = {
                'item_id': item_id,
                'type': 'item',
                'collection_id': coll_id,
                'properties': merged_properties
            }

        output = {
            'id': item_id,
            'body': body
        }

        # Output the item
        self.output(filepath, source_media, output, namespace='items')

        # Check to see if coll_id is in the LRU Cache and skip if true.
        if self.header_deduplication:
            self.collection_id_cache.update({coll_id: None})
            if coll_id in list(self.collection_id_cache.keys()):
                return

        header = {
            'collection_id': coll_id,
            'filepath': filepath
        }

        # Output the header
        self.output(filepath, source_media, header, namespace='header')
