"""
The test module for :mod:`algos.io` .
"""
import io
import pytest
from algos.io import ReadStdIn


data__integer__expected_input = [
    ("1", 1),
    ("-1", -1),
    ("0", 0),
    ("1000000000000000000000", 1000000000000000000000)
]
"""
Test cases for :class:`.ReadStdIn`, testing that it functions correctly for expected inputs.
"""


class TestReadStdIn:
    """
    Test cases for :class:`.ReadStdIn`.
    """
    @pytest.mark.parametrize(
        "test_input,expected",
        data__integer__expected_input,
        ids=[repr(v) for v in data__integer__expected_input]
    )
    def test_integer__expected_input(self, monkeypatch, test_input, expected):
        """
        Test that the integer method works properly for expected inputs.
        """
        # Monkeypatch stdin to hold the value we want the program to read as input
        monkeypatch.setattr('sys.stdin', io.StringIO(test_input))

        # Create the instance
        reader = ReadStdIn()

        # Check that the value is the same as the monkeypatched value
        assert reader.integer() == expected
