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
    def anagrams(self):
        reader: ReadStdIn = ReadStdIn()
        words: str = reader.string()
        words_set = set(" ".join(words).split())

        result: list[list[str]] = anagrams(words_set)
        print(result)
