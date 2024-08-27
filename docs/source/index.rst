Welcome to jsonyx's Documentation!
==================================

.. meta::
    :google-site-verification: Htf0oc5j12UrWDfRoSv2B_0mn4S_mJ2P7eFiE63wwgg

:mod:`jsonyx` is a robust `JSON <http://json.org>`_ manipulator for Python
3.10+. It is written in pure Python with an optional C extension for better
performance and no dependencies.

Key Features:

- JSON decoding, encoding and patching
- Optionally supports these JSON deviations

    .. code-block:: javascript

        {
            /* Block */ // and line comments
            "Decimal numbers": [1.0000000000000001, 1e400],
            "Duplicate keys": {"key": "value 1", "key": "value 2"},
            "Missing commas": [1 2 3],
            "NaN and infinity": [NaN, Infinity, -Infinity],
            "Trailing comma": [0,],
            "Surrogates": "\ud800"
        }

- Detailed error messages

    .. code-block:: pytb

        File "C:\Users\wanne\Downloads\broken.json", line 2, column 15-19
            "path": "c:\users"
                         ^^^^
        jsonyx.JSONSyntaxError: Expecting 4 hex digits

- Dedicated functions for reading and writing files and pretty printing

Check out the :doc:`get-started` section for further information, including how
to :ref:`installation` the project.

.. toctree::
    :hidden:

    get-started
    how-to
    api/index
    cli

.. toctree::
    :caption: About the Project
    :hidden:

    changelog
    License <https://github.com/nineteendo/jsonyx/blob/main/LICENSE>

.. toctree::
    :caption: Project Links
    :hidden:

    PyPI project <https://pypi.org/project/jsonyx>
    GitHub repo <https://github.com/nineteendo/jsonyx>
    Issue Tracker <https://github.com/nineteendo/jsonyx/issues>
