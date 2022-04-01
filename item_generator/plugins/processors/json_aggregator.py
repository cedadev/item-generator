from asset_scanner.core.processor import BaseAggregationProcessor
from asset_scanner.core.types import SpatialExtent, TemporalExtent

import json
import os

from typing import Optional, List, Dict

class JSONAggregator(BaseAggregationProcessor):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.filepath = kwargs['filepath']

    def get_facet_values(self, facet: str, file_id: str) -> List:

        facet_values = []

        with open(self.filepath, 'r') as file:
            file_data = json.load(file)

            for asset in file_data:
                if 'hidden' in asset['body']['categories']:
                    next
                if asset['body']['item_id'] == file_id:
                    values = asset['body']['properties'][facet]
                    if isinstance(values, list):
                        facet_values.extend(values)
                    else:
                        facet_values.append(values)
        return list(set(facet_values))


    def run(self, file_id: str, description: 'ItemDescription') -> dict:

        facets = set(description.facets.aggregation_facets + description.facets.search_facets)

        summaries = {}
        
        for facet in facets:
            values = self.get_facet_values(facet, file_id)
            if values:
                summaries[facet] = values
        body = {
            "properties": summaries
        }
        return body
