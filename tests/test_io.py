"""
The test module for :mod:`algos.io` .
"""
import io
import textwrap
import pytest
from algos.io import ReadStdIn


class DataReadStdIn:
    integer__expected = [
        ("1", 1),
        ("-1", -1),
        ("0", 0),
        ("1000000000000000000000", 1000000000000000000000)
    ]
    """
    Test cases for :meth:`.ReadStdIn.integer`, testing that it functions correctly for expected inputs.
    """

    integer__unexpected = [
        ("a", ValueError),
        ("", ValueError),
        ("0.01", ValueError)
    ]
    """
    Test cases for :meth:`.ReadStdIn.integer`, testing that it raises an error for unexpected inputs.
    """

    array__expected = [
        (("int", "1 2 3"), [1, 2, 3]),
        (("float", "1.0 2.0 3.0"), [1.0, 2.0, 3.0]),
        (("float", "1.0 2 3"), [1.0, 2.0, 3.0]),
        (("str", "a b c"), ["a", "b", "c"]),
        (("str", "1 2 3"), ["1", "2", "3"]),
        (("str", "apple banana carrot"), ["apple", "banana", "carrot"])
    ]
    """
    Test cases for :meth:`.ReadStdIn.array`, testing that it functions correctly for expected inputs.
    """

    array__unexpected = [
        (("int", "1 2 a"), ValueError),
        (("int", ""), ValueError),
        (("int", "1 2 3.0"), ValueError),
        (("float", "1 2 a"), ValueError),
        (("hello", "a b c"), ValueError)
    ]
    """
    Test cases for :meth:`.ReadStdIn.array`, testing that it raises an error for unexpected inputs.
    """

    matrix__expected = [
        (
            (3, "1 2 3\n4 5 6\n7 8 9"),
            [[1, 2, 3],
             [4, 5, 6],
             [7, 8, 9]]
        ),
        (
            (2, "1 2\n4 6"),
            [[1, 2],
             [4, 6]]
        ),
    ]
    """
    Test cases for :meth:`.ReadStdIn.matrix`, testing that it functions correctly for expected inputs.
    """


class TestReadStdIn:
    """
    Test cases for :class:`.ReadStdIn`.
    """
    @pytest.mark.parametrize(
        "test_input,expected",
        DataReadStdIn.integer__expected,
        ids=[repr(v) for v in DataReadStdIn.integer__expected]
    )
    def test_integer__expected_input(self, monkeypatch, test_input, expected):
        """
        Test that the :meth:`.ReadStdIn.integer` method works properly for expected inputs. Test input can be found
        in :attr:`DataReadStdIn.integer__expected` .
        """
        # Monkeypatch stdin to hold the value we want the program to read as input.
        monkeypatch.setattr('sys.stdin', io.StringIO(test_input))

        # Create the reader instance.
        reader = ReadStdIn()

        # Check that the value is the same as the monkeypatched value.
        assert reader.integer() == expected

    @pytest.mark.parametrize(
        "test_input,error",
        DataReadStdIn.integer__unexpected,
        ids=[repr(v) for v in DataReadStdIn.integer__unexpected]
    )
    def test_integer__unexpected_input(self, monkeypatch, test_input, error):
        """
        Test that the :meth:`.ReadStdIn.integer` raises exceptions for unexpected inputs. Test input can be found
        in :attr:`DataReadStdIn.integer__unexpected` .
        """
        # Monkeypatch stdin to hold the value we want the program to read as input.
        monkeypatch.setattr('sys.stdin', io.StringIO(test_input))

        # Create the reader instance.
        reader = ReadStdIn()

        # Check that the exception is raised.
        with pytest.raises(error):
            reader.integer()

    @pytest.mark.parametrize(
        "test_input,expected",
        DataReadStdIn.array__expected,
        ids=[repr(v) for v in DataReadStdIn.array__expected]
    )
    def test_array__expected_input(self, monkeypatch, test_input, expected):
        """
        Test that the :meth:`.ReadStdIn.array` method works properly for expected inputs. Test input can be found
        in :attr:`DataReadStdIn.array__expected` .
        """
        # Reassign input array to meaningful names.
        input_type = test_input[0]
        input_str = test_input[1]

        # Monkeypatch stdin to hold the value we want the program to read as input.
        monkeypatch.setattr('sys.stdin', io.StringIO(input_str))

        # Create the reader instance.
        reader = ReadStdIn()

        # Check that the value is the same as the monkeypatched value.
        assert reader.array(input_type) == expected

    @pytest.mark.parametrize(
        "test_input,error",
        DataReadStdIn.array__unexpected,
        ids=[repr(v) for v in DataReadStdIn.array__unexpected]
    )
    def test_array__unexpected_input(self, monkeypatch, test_input, error):
        """
        Test that the :meth:`.ReadStdIn.array` raises exceptions for unexpected inputs. Test input can be found
        in :attr:`DataReadStdIn.array__unexpected` .
        """
        # Reassign input array to meaningful names.
        input_type = test_input[0]
        input_str = test_input[1]

        # Monkeypatch stdin to hold the value we want the program to read as input
        monkeypatch.setattr('sys.stdin', io.StringIO(input_str))

        # Create the reader instance.
        reader = ReadStdIn()

        # Check that the exception is raised.
        with pytest.raises(error):
            reader.array(input_type)

    @pytest.mark.parametrize(
        "test_input,expected",
        DataReadStdIn.matrix__expected,
        ids=[repr(v) for v in DataReadStdIn.matrix__expected]
    )
    def test_matrix__expected_input(self, monkeypatch, test_input, expected):
        """
        Test that the :meth:`.ReadStdIn.matrix` method works properly for expected inputs. Test input can be found
        in :attr:`DataReadStdIn.matrix__expected` .
        """
        # Reassign input array to meaningful names.
        n = test_input[0]
        input_str = test_input[1]

        # Monkeypatch stdin to hold the value we want the program to read as input.
        monkeypatch.setattr('sys.stdin', io.StringIO(input_str))

        # Create the reader instance.
        reader = ReadStdIn()

        # Check that the value is the same as the monkeypatched value.
        assert reader.matrix(n) == expected