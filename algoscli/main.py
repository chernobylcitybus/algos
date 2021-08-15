import argparse
import sys

from algoscli.text import TextCLI
from algoscli.common import parse_arguments


def text():
    # Import the text component functions
    from algoscli.text import component_functions

    # Parse the command line arguments with argparse.
    args: argparse.Namespace = parse_arguments(
        "text",
        "Text related algorithms",
        "See command line group for a list of functions",
        component_functions
    )

    text_instance: TextCLI = TextCLI()

    if sys.argv[1] == "anagrams":
        text_instance.anagrams()
