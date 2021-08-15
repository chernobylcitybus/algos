from algos.text import anagrams
from algos.io import ReadStdIn
from algoscli.common import Function, Component


component_functions: dict[str, list[Function]] = {
    "text": [
        Function(
            "anagrams",
            "Returns and words which are anagrams of each other, from stdin input. Prints the result to stdout",
        )
    ]
}


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
        reader: ReadStdIn = ReadStdIn()
        words: str = reader.string()
        words_set = set(" ".join(words).split())

        result: list[list[str]] = anagrams(words_set)
        print(result)
