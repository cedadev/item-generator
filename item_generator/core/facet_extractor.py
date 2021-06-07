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


from item_generator.item_describer import ItemDescriptions
from .utils import ProcessorLoader, dict_merge

from typing import List, Callable
from item_generator.core.base import BaseProcessor


class FacetExtractor:

    def __init__(self, conf):
        self.item_description = ItemDescriptions(conf['item_descriptions']['root_directory'])
        self.processors = ProcessorLoader('item_generator.facet_extractors')

    def _load_postprocessors(self, processor: dict) -> List[BaseProcessor]:
        """
        Load the post processors for the given processor

        :param processor: Configuration for the processor including any post processors

        :return: List of loaded processors.
        """

        loaded_pprocessors = []

        for pprocessor in processor.get('post_processors', []):
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

            # Load the processors
            p = self._load_processor(processor)
            post_processors = self._load_postprocessors(processor)

            # Retrieve the metadata
            metadata = p.process(filepath, source_media=source_media, post_processors=post_processors)

            # Merge the extracted metadata with the metadata already retrieved
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
