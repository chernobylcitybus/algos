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
Test cases for :meth:`.ReadStdIn.integer`, testing that it functions correctly for expected inputs.
"""

data__integer__unexpected_input = [
    ("a", ValueError),
    ("", ValueError),
    ("0.01", ValueError)
]
"""
Test cases for :meth:`.ReadStdIn.integer`, testing that it raises an error for unexpected inputs.
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
        Test that the :meth:`.ReadStdIn.integer` method works properly for expected inputs.
        """
        # Monkeypatch stdin to hold the value we want the program to read as input
        monkeypatch.setattr('sys.stdin', io.StringIO(test_input))

        # Create the instance
        reader = ReadStdIn()

        # Check that the value is the same as the monkeypatched value
        assert reader.integer() == expected

    @pytest.mark.parametrize(
        "test_input,error",
        data__integer__unexpected_input,
        ids=[repr(v) for v in data__integer__unexpected_input]
    )
    def test_integer__unexpected_input(self, monkeypatch, test_input, error):
        """
        Test that the :meth:`.ReadStdIn.integer` raises exceptions for unexpected inputs.
        """
        # Monkeypatch stdin to hold the value we want the program to read as input
        monkeypatch.setattr('sys.stdin', io.StringIO(test_input))

        # Create the instance
        reader = ReadStdIn()

        with pytest.raises(error):
            reader.integer()
