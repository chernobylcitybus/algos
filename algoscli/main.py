"""
This module yields the command line entry points to the algorithms in :any:`algos` . Each function in this module
corresponds to an equivalent command line grouping. The command line groupings thus far are

+--------------------------------+-------------------------------------------------------------------------------+
| Name                           | purpose                                                                       |
+================================+===============================================================================+
| :func:`.text`                  | Expose the text algorithms. Represents :code:`algos-text` command line group. |
+--------------------------------+-------------------------------------------------------------------------------+

All algorithms read input data through ``stdin`` . A typical usage would be

.. code-block:: bash

   echo "the elbow on the arc is below the car" | algos-text anagrams
   [['arc', 'car'], ['elbow', 'below']]

"""
import argparse
import sys
from collections.abc import Callable
from typing import Optional

from algoscli.text import TextCLI
from algoscli.common import parse_arguments


def text():
    """
    The main entrypoint for text based algorithms. The currently supported algorithms are

    +-----------------------------------------+
    | :func:`algos.text.anagrams`             |
    +-----------------------------------------+

    :raises ValueError: If the subcommand is not recognized.

    """
    # Import the text component functions
    from algoscli.text import component_functions

    # Parse the command line arguments with argparse.
    args: argparse.Namespace = parse_arguments(
        "text",
        "Text related algorithms",
        "See command line group for a list of functions",
        component_functions
    )

    # Create a TextCLI instance for the subcommand handlers.
    text_instance: TextCLI = TextCLI()

    # Create a dictionary so that we don't have a massive if-else statement to choose the subcommand handler.
    handlers: dict[str, Callable[[], None]] = {"anagrams": text_instance.anagrams}

    # Get the appropriate handler, depending on sys.argv[1] .
    handler: Optional[Callable[[], None]] = handlers.get(sys.argv[1], None)

    # Handle the case of an unrecognized command.
    if handler is None:
        raise ValueError("Unknown subcommand " + sys.argv[1])

    # Execute command line.
    handler()
