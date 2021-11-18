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

from item_generator.extraction_methods import utils as item_utils

LOGGER = logging.getLogger(__name__)

from typing import List


class FacetExtractor(BaseExtractor):
    PROCESSOR_ENTRY_POINT = 'item_generator.facet_extractors'

    def __init__(self, conf: dict):
        super().__init__(conf)

        self.pre_processors = self.load_processors(entrypoint='item_generator.pre_processors')
        self.post_processors = self.load_processors(entrypoint='item_generator.post_processors')

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

            loaded = self._get_processor(pp_name, key, **pp_kwargs)

            if loaded:
                loaded_pprocessors.append(loaded)

        return loaded_pprocessors

    def _load_processor(self, processor: dict) -> BaseProcessor:
        processor_name = processor['name']
        processor_inputs = processor.get('inputs', {})
        output_key = processor.get('output_key')

        return self._get_processor(
            processor_name,
            'processors',
            output_key=output_key,
            **processor_inputs
        )

    def _get_processor(self, name: str, group: str = 'processors', **kwargs) -> BaseProcessor:
        """

        :param name: Name of the requested processor
        :return: processor object
        """

        return getattr(self, group).get_processor(name, **kwargs)

    def _run_processor(self, processor: dict, filepath: str, source_media: StorageType) -> dict:
        """Run the specified processor."""

        # Load the processors
        p = self._load_processor(processor)
        pre_processors = self._load_extra_processors(processor, 'pre_processors')
        post_processors = self._load_extra_processors(processor, 'post_processors')

        # Retrieve the metadata
        metadata = p.run(filepath, source_media=source_media, post_processors=post_processors,
                         pre_processors=pre_processors)

        output_key = getattr(p, 'output_key', None)

        if output_key and metadata:
            metadata = dot2dict(output_key, metadata)

        return metadata
    
    def get_collection_id(self, description: ItemDescription, filepath: str, storage_media: StorageType) -> str:
        """Return the collection ID for the file."""
        collections_id_def = getattr(description.collections, 'id', None)
        collection_id = 'undefined'

        if collections_id_def:

            # Retrieve defaults
            tags = collections_id_def.defaults

            # Run the processors
            for processor in collections_id_def.extraction_methods:
                metadata = self._run_processor(processor, filepath, storage_media)

                if metadata:
                    tags = dict_merge(tags, metadata)

            # Check to see if we have pulled out a collection id
            generated_id = tags.get('collection_id')

            if generated_id:
                collection_id = generated_id

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

            metadata = self._run_processor(processor, filepath, source_media)

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

        # Get collection id
        coll_id = self.get_collection_id(description, filepath, source_media)

        # Generate item id
        item_id = item_utils.generate_item_id_from_properties(
            filepath,
            coll_id,
            processor_output.get('properties', {}),
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
