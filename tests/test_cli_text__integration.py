"""
The integration test module for :func:`algoscli.main.text` . The command line as it would appear in the shell is tested
using subprocesses. Its output is captured and then compared to the expected values.
"""
import subprocess
import pytest


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
    def test_anagrams__expected(self, test_input, expected):
        """
        Test that the :func:`algoscli.text.TextCLI.anagrams` function works properly for expected inputs. Test input can be found
        in :attr:`DataText.anagrams__expected` .
        """
        # stdin input
        stdin_input = " ".join(list(test_input))

        # Run a subprocess with the command line
        captured = subprocess.check_output("echo \"" + stdin_input + "\" | algos-text anagrams", shell=True)

        # Decode to string.
        if isinstance(captured, bytes):
            captured = captured.decode()

        # Sort in order to compare generated anagrams against expected value.
        anagrams_found = eval(captured)
        anagrams_found = [sorted(x) for x in anagrams_found]
        anagrams_found.sort()

        # Check that the output is as expected.
        assert anagrams_found == expected

