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

LOGGER = logging.getLogger(__name__)

from typing import List
from string import Template


class FacetExtractor(BaseExtractor):

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

    def process_file(self, filepath, source_media, **kwargs):
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

        # Do not run processors if the asset has been marked as hidden. This
        # prevents files like .ftpaccess files from becoming STAC items
        categories = self.get_categories(filepath, source_media, description)
        if 'hidden' in categories:
            return

        processor_output = self.run_processors(filepath, description, source_media, **kwargs)
        properties = processor_output.get('properties', {})

        # Generate title and description properties from templates
        templates = description.facets.templates

        if properties and templates:
            if templates.title_template:
                title_template = templates.title_template
                title = Template(title_template).safe_substitute(properties)
                properties['title'] = title
            if templates.description_template:
                desc_template = templates.description_template
                desc = Template(desc_template).safe_substitute(properties)
                properties['description'] = desc

        # Get collection id
        coll_id = self.get_collection_id(description, filepath, source_media)

        # Generate item id
        item_id = item_utils.generate_item_id_from_properties(
            filepath,
            coll_id,
            properties,
            description
        )

        base_item_dict = {
                'item_id': item_id,
                'type': 'item',
                'collection_id': coll_id
            }

        # Merge processor output with base defaults
        body = dict_merge(base_item_dict, processor_output)

        output = {
            'id': item_id,
            'body': body
        }

        # Output the item
        self.output(filepath, source_media, output, namespace='facets')

        # Add item id to asset
        output = {
            'id': file_id,
            'body': {
                'item_id': item_id
            }
        }

        self.output(filepath, source_media, output, namespace='assets')
