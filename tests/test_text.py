"""
The test module for :mod:`algos.text` .
"""
import pytest
from algos.text import anagrams


class DataText:
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
    @pytest.mark.parametrize(
        "test_input,expected",
        DataText.anagrams__expected,
        ids=[str(v) for v in range(len(DataText.anagrams__expected))]
    )
    def test_anagrams__expected(self, test_input, expected):
        """
        Test that the :func:`.anagrams` function works properly for expected inputs. Test input can be found
        in :attr:`DataText.anagrams__expected` .
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
        Test that the :func:`.anagrams` raises exceptions for unexpected inputs. Test input can be found
        in :attr:`DataText.anagrams__unexpected` .
        """
        # Check if error is raised.
        with pytest.raises(error):
            anagrams(test_input)
