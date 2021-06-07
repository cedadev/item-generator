# encoding: utf-8
"""

Configuration Options:

    item_descriptions:
        ``root_directory``: Path to the root directory for the item description yaml files

        example:

            ..code-block:: yaml

                item_descriptions:
                    root_directory: /path/to/descriptions

    logging:
        keyword arguments to pass to the python ``logging.basicConfig`` method

"""
__author__ = 'Richard Smith'
__date__ = '04 Jun 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

import argparse
import yaml
from item_generator import FacetExtractor

import logging


def cmd_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('conf', help='Path to config file')

    args = parser.parse_args()

    return args


def load_config(path):
    with open(path) as reader:
        conf = yaml.safe_load(reader)

    return conf


def setup_logging(conf):

    config = conf.get('logging', {})
    if not config or (config and not config.get('format')):
        config['format'] = '%(asctime)s %(name)s %(levelname)s %(message)s'

    logging.basicConfig(**config)


def main():

    args = cmd_arguments()

    conf = load_config(args.conf)
    
    setup_logging(conf)
    
    extractor = FacetExtractor(conf)

    extractor.process_file('/badc/faam/data/2005/b069-jan-05/core_processed/core_faam_20050105_r0_b069.nc', 'POSIX')
