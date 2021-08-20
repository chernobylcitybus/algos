"""
This module yields the command line entry points to the algorithms in :mod:`algos.text` . The :class:`TextCli` class
corresponds to the ``algos-text`` command line interface. The list of methods and their purposes are described below.

+--------------------------------+-------------------------------------------------------------------------------+
| Name                           | purpose                                                                       |
+================================+===============================================================================+
| :meth:`.TextCli.anagrams`      | Finds all the anagrams in the given input.                                    |
+--------------------------------+-------------------------------------------------------------------------------+

"""
from algos.text import anagrams
from algos.io import ReadStdIn
from algoscli.common import Function


component_functions: dict[str, list[Function]] = {
    "text": [
        Function(
            "anagrams",
            "Returns and words which are anagrams of each other, from stdin input. Prints the result to stdout",
        )
    ]
}
"""
The list values are the subcommands to the ``algos-text`` command line group. The information is used by argparse to
check the command line input against the expected arguments for the sub commands. The :class:`.Function` s also contain
the help information to be displayed by :mod:`argparse` .
"""


class TextCLI:
    """
    Class that wraps text command line functionality.
    """
    def anagrams(self) -> None:
        """
        Reads character input from stdin and finds all words which are anagrams of each other in the input string.
        Prints to stdout.

        A typical usage might be

        .. code-block:: bash

           echo "below on the elbow is the bowel" | algos-text anagrams
           [['elbow', 'below', 'bowel']]

        """
        # Generate an instance of ReadStdIn.
        reader: ReadStdIn = ReadStdIn()

        # Read stdin and create set of words for anagrams.
        words: list[str] = reader.string()
        words_set = set(" ".join(words).split())

        # If the input is empty, just pass in the empty set.
        if len(words_set) == 0:
            words_set = {""}

        # Call the function.
        result: list[list[str]] = anagrams(words_set)

        # Print results to stdout.
        print(result)
