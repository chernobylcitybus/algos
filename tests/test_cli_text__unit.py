"""
The unit test module for :mod:`algoscli.main.text` . Command line stdin input is essentially mocked and we capture
standard output through capsys to verify the results.
"""
import io
import re
import argparse
import sys
import pytest
from unittest.mock import patch
from algoscli.main import text


class DataText:
    """
    Test data for text based algorithms. Contains lists of tuples of the form (inputs, expected). The data for the
    following functions is contained within

    +--------------------------------------+
    | anagrams                             |
    +--------------------------------------+

    """
    anagrams__expected = [
        (
            {'the', 'car', 'can', 'caused', 'a', 'and', 'during', 'cried', 'by', 'its', 'rat', 'bowel', 'drinking',
             'elbow', 'bending', 'that', 'while', 'an', 'thing', 'cider', 'like', 'pain', 'cat', 'which', 'in', 'this',
             'act', 'below', 'is', 'night', 'arc'},
            [['act', 'cat'], ['arc', 'car'], ['below', 'bowel', 'elbow'], ['cider', 'cried'], ['night', 'thing']]
        ),
        (
            {"elbow", "below", "bowel"},
            [['below', 'bowel', 'elbow']]
        ),
        (
            {""},
            []
        )
    ]
    """
    Test cases for :func:`algoscli.text.TextCLI.anagrams`, testing that it functions correctly for expected inputs. 
    The test cases are as follows

    +--------------------------------------+----------------------------------------------------------------------+
    | description                          | reason                                                               |
    +======================================+======================================================================+
    | many anagram lists                   | Test to see if multiple lists of anagrams are produced when input    |
    |                                      | set has multiple instances of different words which are anagrams of  |
    |                                      | each other.                                                          |
    +--------------------------------------+----------------------------------------------------------------------+
    | single anagram list                  | Test to see if a single set of anagrams is identified.               |
    +--------------------------------------+----------------------------------------------------------------------+
    | no anagrams                          | Test to see if a non-empty set with no anagrams produces no results  |
    +--------------------------------------+----------------------------------------------------------------------+

    """


class TestAnagrams:
    """
    Test class for :meth:`algoscli.text.TextCLI.anagrams`.
    """
    @pytest.mark.parametrize(
        "test_input,expected",
        DataText.anagrams__expected,
        ids=[str(v) for v in range(len(DataText.anagrams__expected))]
    )
    def test_anagrams__expected(self, monkeypatch, capsys, test_input, expected):
        """
        Test that the :func:`algoscli.text.TextCLI.anagrams` function works properly for expected inputs. Test input
        can be found in :attr:`DataText.anagrams__expected` .

        We patch :attr:`sys.argv` with our desired command line inputs and monkeypatch ``stdin`` with our desired
        text input stream.
        """
        # Command line arguments
        cli_argv = ["algos-text", "anagrams"]

        # stdin input
        stdin_input = " ".join(list(test_input))

        # Monkeypatch stdin to hold the value we want the program to read as input.
        monkeypatch.setattr('sys.stdin', io.StringIO(stdin_input))

        # Patch sys.argv to have correct cli arguments.
        with patch.object(sys, "argv", cli_argv):
            # Find the anagrams.
            text()
            captured = capsys.readouterr()

        # Sort in order to compare generated anagrams against expected value.
        anagrams_found = eval(captured.out)
        anagrams_found = [sorted(x) for x in anagrams_found]
        anagrams_found.sort()

        # Check that the output is as expected.
        assert anagrams_found == expected


class TestText:
    """
    Test functionality specific to command line handler.
    """
    def test_invalid_subcommand(self):
        """
        Check that the :func:`algoscli.main.text` raises :class:`argparse.ArgumentError` when an invalid subcommand is
        given.

        We patch sys.argv to put in our desired command line arguments, sys.exit in order to stop argparse from
        exiting and then we try to raise the exception for an invalid subcommand.
        """
        # Command line arguments
        cli_argv = ["algos-text", "does_not_exist"]

        # Patch sys.argv to have correct cli arguments.
        with patch.object(sys, "argv", cli_argv):
            # Patch exit as argparse calls exit on non matching command line.
            with patch.object(sys, "exit", lambda x: 0):
                # Try to raise the exception
                with pytest.raises(ValueError) as excinfo:
                    text()
                # Check that we raised the expected exception by matching the exception string.

                assert excinfo.match(re.escape("Unknown subcommand does_not_exist"))
