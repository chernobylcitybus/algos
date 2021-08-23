"""
Tests for :mod:`algoscli.common`. Primarily deal with command line processing.
"""
import argparse
import pytest
import sys
from unittest.mock import patch
from algoscli.common import Function, parse_arguments

component_functions: dict[str, list[Function]] = {
    "text": [
        Function(
            "anagrams",
            "Returns and words which are anagrams of each other, from stdin input. Prints the result to stdout",
        )
    ]
}
"""
Example components for :func:`.parse_arguments` . No arguments.
"""

component_functions2: dict[str, list[Function]] = {
    "text": [
        Function(
            "anagrams",
            "Returns and words which are anagrams of each other, from stdin input. Prints the result to stdout",
            args=[
                ("eval", "Eval the input.")
            ]
        )
    ]
}
"""
Example components for :func:`.parse_arguments` . With arguments.
"""

component_functions3: dict[str, list[Function]] = {
    "text": [
        Function(
            "anagrams",
            "Returns and words which are anagrams of each other, from stdin input. Prints the result to stdout",
            args=[
                ("--eval", "Eval the input.")
            ]
        )
    ]
}
"""
Example components for :func:`.parse_arguments` . With optional arguments.
"""


def test_parse_arguments_none():
    """
    Test the :func:`.parse_arguments` where there are no named command line inputs. Uses :data:`component_functions`.

    We patch :attr:`sys.argv` and call parse_arguments to see that it correctly processes the component functions.
    """
    cli_argv = ["algos-text", "anagrams"]

    with patch.object(sys, "argv", cli_argv):
        args = parse_arguments(
            "text",
            "Some description",
            "Some help",
            component_functions
        )

    assert isinstance(args, argparse.Namespace)


def test_parse_arguments_args():
    """
    Test the :func:`.parse_arguments` where there are named command line inputs. Uses :data:`component_functions2`.

    We patch :attr:`sys.argv` and call parse_arguments to see that it correctly processes the component functions. We
    also check if the given command line arguments are accessible within the returned namespace, and have the correct
    values that were supplied.
    """
    cli_argv = ["algos-text", "anagrams", "True"]

    with patch.object(sys, "argv", cli_argv):
        args = parse_arguments(
            "text",
            "Some description",
            "Some help",
            component_functions2
        )

    assert args.eval == "True"


def test_parse_arguments_args_optional():
    """
    Test the :func:`.parse_arguments` where there are named command line inputs. Uses :data:`component_functions3`.

    We patch :attr:`sys.argv` and call parse_arguments to see that it correctly processes the component functions. We
    also check if the given command line arguments are accessible within the returned namespace, and have the correct
    values that were supplied.
    """
    cli_argv = ["algos-text", "anagrams", "--eval"]

    with patch.object(sys, "argv", cli_argv):
        args: argparse.Namespace = parse_arguments(
            "text",
            "Some description",
            "Some help",
            component_functions3
        )

    assert args.eval is True
