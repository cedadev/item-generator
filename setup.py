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
    test_suite='tests',
    install_requires=[
        'asset_scanner',
        'directory_tree',
        'python-dateutil'
    ],
    tests_require=[
        'pytest',
        'tox'
    ],
    extras_require={
        'docs': [
            'sphinx',
            'sphinx-rtd-theme',
            'sphinx_fontawesome',
            'sphinxcontrib-programoutput'
        ],
        'dev': [
            'isort'
        ]
    },
    entry_points={
        'console_scripts': [
            'generate_items = item_generator.scripts.extract_facet:main',
        ],
        'asset_scanner.extractors': [
          'item_generator = item_generator:FacetExtractor'
        ],
        'item_generator.facet_extractors': [
            'regex = item_generator.extraction_methods.regex_extract:RegexExtract',
            'header_extract = item_generator.extraction_methods.header_extract.header_extract:HeaderExtract'
        ],
        'item_generator.facet_extractors.header_extract.backends': [
            'xarray = item_generator.extraction_methods.header_extract.backends.xarray:XarrayBackend',
            'cf = item_generator.extraction_methods.header_extract.backends.cf:CfBackend'
        ],
        'item_generator.pre_processors': [
            'filename_reducer = item_generator.extraction_methods.preprocessors:ReducePathtoName'
        ],
        'item_generator.post_processors': [
            'isodate_processor = item_generator.extraction_methods.postprocessors:ISODateProcessor',
        ]
    }
)
