Welcome to jsonyx's Documentation!
==================================

.. meta::
    :google-site-verification: Htf0oc5j12UrWDfRoSv2B_0mn4S_mJ2P7eFiE63wwgg

:mod:`jsonyx` is a customizable `JSON <https://json.org>`_ library for Python
3.8+. It is written in pure Python with an optional C extension for better
performance and no dependencies.

Key Features
------------

- JSON decoding, encoding and patching
- Pretty-printing:

  .. code-block:: json

      {
          "foo": [1, 2, 3],
          "bar": {"a": 1, "b": 2, "c": 3}
      }

- Optionally supports these JSON deviations (according to
  :doc:`this specification </jsonyx-spec>`):

  .. code-block:: javascript

      {
          /* Block */ // and line comments
          "Missing commas": [1 2 3],
          "NaN and infinity": [NaN, Infinity, -Infinity],
          "Surrogates": "\ud800",
          "Trailing comma": [0,],
          "Unquoted keys": {key: "value"}
      }

- Detailed error messages:

  .. code-block:: none

      Traceback (most recent call last):
        File "/Users/wannes/Downloads/broken.json", line 1, column 99-381
          ...sList": {"GlossEntry": {"ID": "SGM..."GML", "XML"]}, "GlossSee": "markup"
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      jsonyx.JSONSyntaxError: Unterminated object

Check out the :doc:`/get-started` section for further information, including
how to :ref:`install <installation>` the project.

.. _end_forword:

.. toctree::
    :hidden:

    Home <self>

.. _start_toctree:

.. toctree::
    :hidden:

    get-started
    how-to
    benchmark
    api/index
    cli/index

.. toctree::
    :caption: Specification
    :hidden:

    jsonyx-spec
    json-patch-spec
    json-path-spec

.. toctree::
    :caption: About the Project
    :hidden:

    changelog
    License <https://github.com/nineteendo/jsonyx/blob/main/LICENSE>

.. toctree::
    :caption: Project Links
    :hidden:

    PyPI Package <https://pypi.org/project/jsonyx>
    Conda Package <https://anaconda.org/conda-forge/jsonyx>
    GitHub Repository <https://github.com/nineteendo/jsonyx>
    Issue Tracker <https://github.com/nineteendo/jsonyx/issues>
    Sponser <https://paypal.me/nineteendo>
