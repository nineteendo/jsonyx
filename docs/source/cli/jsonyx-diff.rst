jsonyx diff
===========

.. program:: jsonyx diff

Compare two JSON files and generate a diff in JSON patch format.

Usage
-----

.. code-block:: none

    jsonyx diff [-h] [-a] [-c] [-C] [-d] [-i SPACES] [-l] [-L LEVEL] [-s] [-S]
                [-t] [-T] [-q] old_input_filename [input_filename]
                [output_filename]

Positional arguments
--------------------

.. option:: old_input_filename

    The path to the old input JSON file.

.. option:: input_filename

    The path to the input JSON file, or ``"-"`` for standard input. If not
    specified, read from :data:`sys.stdin`.

.. option:: output_filename

    The path to the output :doc:`JSON patch </json-patch-spec>` file. If not
    specified, write to :data:`sys.stdout`.

See :doc:`/cli/jsonyx-format` for the formatting options.
