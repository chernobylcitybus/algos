"""
The test module for :mod:`algoscli.main.test` .
"""
import io
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
    Test cases for :func:`.anagrams`, testing that it functions correctly for expected inputs.
    """

    anagrams__unexpected = [
        (set(), ValueError),
        (["hello"], TypeError),
        ({1, 2, 3}, TypeError)
    ]
    """
    Test cases for :func:`.anagrams`, testing that it raises an error for unexpected inputs.
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
        Test that the :func:`.anagrams` function works properly for expected inputs. Test input can be found
        in :attr:`DataText.anagrams__expected` .
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

