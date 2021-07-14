.. _processors:


******************
Processors
******************

Processors take a file and return a dictionary of extracted information. They
can be chained, one after the other and the results are merged such that arrays
are appended to and key:value pairs are overwritten by subsequent write operations.

Some processors can also take :ref:`pre-processors` and :ref:`post-processors`. Pre-processors modify
the input arguments whilst post-processors modify the output from the main processor.

.. list-table::
    :header-rows: 1

    * - Processor Name
      - Description
    * - :ref:`header_extract <header-extract>`
      - Takes a filepath string and a list of attributes and returns a dictionary of the values extracted from the file header.
    * - :ref:`regex <regex>`
      - Takes an input string and a regex with named capture groups and returns a dictionary of the values extracted using the named capture groups.


.. automodule:: item_generator.extraction_methods.header_extract

.. autoclass:: item_generator.extraction_methods.header_extract.HeaderExtract

.. automodule:: item_generator.extraction_methods.regex_extract
    :members:


.. _pre-processors:

Pre Processors
==============

.. automodule:: item_generator.extraction_methods.preprocessors

.. list-table::
    :header-rows: 1

    * - Processor Name
      - Description
    * - :ref:`filename_reducer <filename-reducer>`
      - Takes a file path and returns the filename using ``os.path.basename``.

.. _filename-reducer:

Filename Reducer
----------------

.. autoclass:: item_generator.extraction_methods.preprocessors.ReducePathtoName



.. _post-processors:

Post Processors
===============

.. automodule:: item_generator.extraction_methods.postprocessors

.. list-table::
    :header-rows: 1

    * - Processor Name
      - Description
    * - :ref:`facet_map <facet-map>`
      - In some cases, you may wish to map the header attributes to different facets. This method takes a map and converts the facet labels into those specified.
    * - :ref:`isodate_processor <isodate-processor>`
      - Takes the source dict and the key to access the date and converts the date to ISO 8601 Format.

.. _facet-map:

Facet Map Processor
-------------------

.. autoclass:: item_generator.extraction_methods.postprocessors.FacetMapProcessor

.. _isodate-processor:

ISO Date Processor
-------------------
.. autoclass:: item_generator.extraction_methods.postprocessors.ISODateProcessor
