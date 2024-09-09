Welcome to jsonyx's Documentation!
==================================

.. meta::
    :google-site-verification: Htf0oc5j12UrWDfRoSv2B_0mn4S_mJ2P7eFiE63wwgg

:mod:`jsonyx` is a customizable `JSON <http://json.org>`_ library for Python
3.10+. It is written in pure Python with an optional C extension for better
performance and no dependencies.

.. rubric:: Key Features

- JSON decoding, encoding and patching
- Pretty-printing:

.. code-block:: json

    {
        "foo": [1, 2, 3],
        "bar": {"a": 1, "b": 2, "c": 3}
    }

- Optionally supports these JSON deviations using :mod:`jsonyx.allow`:

.. code-block:: javascript

    {
        /* Block */ // and line comments
        "Decimal numbers": [1.0000000000000001, 1e400],
        "Duplicate keys": {"key": "value 1", "key": "value 2"},
        "Missing commas": [1 2 3],
        "NaN and infinity": [NaN, Infinity, -Infinity],
        "Surrogates": "\ud800",
        "Trailing comma": [0,],
        "Unquoted keys": {key: "value"}
    }

- Detailed error messages:

.. code-block:: none

    Traceback (most recent call last):
      File "C:\Users\wanne\Downloads\broken.json", line 2, column 15-19
        "path": "c:\users"
                     ^^^^
    jsonyx.JSONSyntaxError: Expecting 4 hex digits

- Dedicated functions for reading and writing files and pretty printing

.. rubric:: Benchmark

We recommend to use ``orjson`` for performance critical applications:

=====================================================  ========  ========  =========  ========  ===========  ============  ========  ===========
encode                                                     json    jsonyx    msgspec    orjson    rapidjson    simplejson     ujson    unit (μs)
=====================================================  ========  ========  =========  ========  ===========  ============  ========  ===========
Array with 256 doubles                                 26.2424   25.4066     1.40231         1     25.132        24.065     5.09411      8.67893
Array with 256 UTF-8 strings                           25.4609   11.2325     2.21991         1     31.6519       19.521    12.4357      14.3079
Array with 256 strings                                 12.6682   11.5845     1.48954         1      8.99742      13.594     6.28623      4.2012
Medium complex object                                   9.75149  12.1889     1.21726         1      7.26384      15.4871    5.37233     14.7212
Array with 256 True values                              4.69641   3.99912    1.18751         1      3.22802       7.00218   5.15626      1.81105
Array with 256 dict{string, int} pairs                 10.7704   24.2856     1.45873         1      6.34784      33.7662    6.28966      8.55489
Dict with 256 arrays with 256 dict{string, int} pairs   8.68721  18.9343     1.23578         1      5.01594      29.1285    5.47603   2703.46
Complex object                                          8.21073   7.22957    1             inf      7.04675      10.1288    4.60132    200.052
=====================================================  ========  ========  =========  ========  ===========  ============  ========  ===========

=====================================================  =======  ========  =========  ========  ===========  ============  =======  ===========
decode                                                    json    jsonyx    msgspec    orjson    rapidjson    simplejson    ujson    unit (μs)
=====================================================  =======  ========  =========  ========  ===========  ============  =======  ===========
Array with 256 doubles                                 6.61055   6.94454    1.50775   1            5.7042        6.60096  2.888       10.3663
Array with 256 UTF-8 strings                           1         1.12574    2.58121   1.98783      2.96541       1.27757  2.02365     65.8555
Array with 256 strings                                 1.63882   1.61365    1.11284   1            1.55679       2.29262  2.57514     13.64
Medium complex object                                  2.51619   3.18186    2.78223   1            9.77177       3.57637  1.96885     41.1542
Array with 256 True values                             3.51618   5.10572    2.09131   1            2.39643       4.00223  2.15635      2.19626
Array with 256 dict{string, int} pairs                 2.39741   2.94758    1.4098    1            2.24916       3.39941  1.68995     31.8937
Dict with 256 arrays with 256 dict{string, int} pairs  1.60704   1.85267    1.13059   1            1.45558       1.91914  1.03881  17923.3
Complex object                                         1.22359   1.14545    1.17331   1.08619      1.3403        1.4094   1          979.498
=====================================================  =======  ========  =========  ========  ===========  ============  =======  ===========

Check out the :doc:`get-started` section for further information, including how
to :ref:`install <installation>` the project.

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

    PyPI Package <https://pypi.org/project/jsonyx>
    Conda Package <https://anaconda.org/conda-forge/jsonyx>
    GitHub Repository <https://github.com/nineteendo/jsonyx>
    Issue Tracker <https://github.com/nineteendo/jsonyx/issues>
    Sponser <https://paypal.me/nineteendo>
