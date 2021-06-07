# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '27 May 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    _long_description = readme_file.read()

setup(
    name='item_generator',
    description='Extracts facets from the individual files and generates an identifier which can be used to aggregate',
    author='Richard Smith',
    url='https://github.com/cedadev/item-generator/',
    long_description=_long_description,
    long_description_content_type='text/markdown',
    license='BSD - See asset_extractor/LICENSE file for details',
    packages=find_packages(),
    package_data={
        'item_generator': [
            'LICENSE'
        ]
    },
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'generate_items = item_generator.scripts.extract_facets:main',
        ],
        'item_generator.facet_extractors': [
            'regex = item_generator.extraction_methods:regex_extract',
            'date_convert = item_generator.extraction_methods.postprocessors:date_convert'
        ]
    }
)
