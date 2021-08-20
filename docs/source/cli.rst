Command Line Interface
======================

This package supports using the :any:`algos` package as a command line interface. The modules and their purposes are
as follows

+--------------------------------------+---------------------------------------------------------------------------+
| module                               | purpose                                                                   |
+======================================+===========================================================================+
| :mod:`algoscli.common`               | Contains common functions for the CLI such as command line parsing.       |
+--------------------------------------+---------------------------------------------------------------------------+
| :mod:`algoscli.main`                 | Contains the entry points for the console scripts.                        |
+--------------------------------------+---------------------------------------------------------------------------+
| :mod:`algoscli.text`                 | Wrappers for the :mod:`algos.text` module to allow calling from shell.    |
+--------------------------------------+---------------------------------------------------------------------------+

.. toctree::

   cli_common
   cli_main
   cli_text
