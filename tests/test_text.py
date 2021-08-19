"""
The test module for :mod:`algos.text` . Consists of a data class :class:`DataText` that stores expected inputs and
outputs for the different text based algorithms. The class also provides data for exception handling tests.

Each function in :mod:`algos.text` is assigned to a test class and the expected inputs and unexpected inputs tests are
performed within. The inputs and outputs are then tested in a parametrized fashion.
"""
import pytest
from algos.text import anagrams


class DataText:
    """
    Holds the data for :mod:`algos.text` .
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
    Test cases for :func:`algos.text.anagrams`, testing that it functions correctly for expected inputs. The test
    cases are as follows
    
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

    anagrams__unexpected = [
        (set(), [ValueError, "Empty Set"]),
        (["hello"], [TypeError, "Input Data Type Not Set"]),
        ({1, 2, 3}, [TypeError, "Not All Elements of Type str"])
    ]
    """
    Test cases for :func:`algos.text.anagrams`, testing that it raises an error for unexpected inputs. The test cases
    are as follows

    +--------------------------------------+----------------------------------------------------------------------+
    | description                          | reason                                                               |
    +======================================+======================================================================+
    | empty set input                      | Check that :class:`ValueError` is raised for empty input             |
    +--------------------------------------+----------------------------------------------------------------------+
    | incorrect input type                 | Check that :class:`TypeError` is raised if input is not a set        |
    +--------------------------------------+----------------------------------------------------------------------+
    | incorrect elements type              | Check that :class:`TypeError` is raised if any element of the set is |
    |                                      | not :class:`str` .                                                   |
    +--------------------------------------+----------------------------------------------------------------------+
    
    """


class TestAnagrams:
    """
    Class to test :func:`algos.text.anagrams` . Holds the expected input tests and exception handlings tests.
    """
    @pytest.mark.parametrize(
        "test_input,expected",
        DataText.anagrams__expected,
        ids=[str(v) for v in range(len(DataText.anagrams__expected))]
    )
    def test_anagrams__expected(self, test_input, expected):
        """
        Test that the :func:`algos.text.anagrams` function works properly for expected inputs. Test input can be found
        in :attr:`DataText.anagrams__expected` along with a description of their purpose.
        """
        # Assign a meaningful name to the test set.
        word_set = test_input

        # Find the anagrams.
        anagrams_found = anagrams(word_set)

        # Sort in order to compare generated anagrams against expected value.
        anagrams_found = [sorted(x) for x in anagrams_found]
        anagrams_found.sort()

        # Check that the output is as expected.
        assert anagrams_found == expected

    @pytest.mark.parametrize(
        "test_input,error",
        DataText.anagrams__unexpected,
        ids=[repr(v) for v in DataText.anagrams__unexpected]
    )
    def test_anagrams__unexpected(self, test_input, error):
        """
        Test that the :func:`algos.text.anagrams` raises exceptions for unexpected inputs. Test input can be found
        in :attr:`DataText.anagrams__unexpected` along with a description of their purpose.
        """
        # Check if error is raised.
        with pytest.raises(error[0]) as excinfo:
            anagrams(test_input)

        assert excinfo.match(error[1])
