jsonyx patch
============

.. program:: jsonyx patch

Apply a JSON patch to the input file.

Usage
-----

.. code-block:: none

    jsonyx patch [-h] [-a] [-c] [-C] [-d] [-i SPACES] [-l] [-L LEVEL] [-s]
                 [-S] [-t] [-T] [-q] patch_filename [input_filename]
                 [output_filename]

Positional arguments
--------------------

.. option:: patch_filename

    The path to the JSON patch file.

.. option:: input_filename

    The path to the input JSON file, or ``"-"`` for standard input. If not
    specified, read from :data:`sys.stdin`.

.. option:: output_filename

    The path to the output JSON file. If not specified, write to
    :data:`sys.stdout`.

See :doc:`/cli/jsonyx-format` for the formatting options.
