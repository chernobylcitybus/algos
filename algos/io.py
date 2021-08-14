"""
A general module that contains a variety of helper classes supporting input/output operations.
"""
import os
import sys
import logging
from typing import TypeVar, Any, Union, Optional


# Set up the logger for the module
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s [%(lineno)d] %(message)s "
)

NumArrTypes = TypeVar("NumArrTypes", list[int], list[float])
"""Generic variable for numeric arrays."""

NumMatTypes = TypeVar("NumMatTypes", list[list[int]], list[list[float]])
"""Generic variable for numeric matrices."""


def flush_buffers_and_exit(error: int) -> None:
    """
    A convenience function to flush stdout and stderr buffers and exit the program with a given OS return value.

    :param int error: An OS return value from :mod:`os`.
    """
    # Flush the buffers.
    sys.stdout.flush()
    sys.stderr.flush()

    # Exit
    sys.exit(error)


def convert_anystr(any_str: Union[str, bytes]) -> str:
    """
    Helper function to take an :class:`.Union[str, bytes]` type and return :class:`str` output. Returns :class:`str` input
    unmodified but decodes :class:`bytes` input to :class:`str`.

    :param typing.Union[str, bytes] any_str: The :class:`str` or :class:`bytes` object to coerce.
    :rtype: str
    :return: :class:`str` value of any_str.
    """
    return_value: Union[str, bytes]
    if isinstance(any_str, str):
        return_value = any_str
    elif isinstance(any_str, bytes):
        return_value = any_str.decode()

    return return_value


class ReadStdIn:
    """
    A class that has multiple methods for reading stdin inputs.

    :ivar logging.Logger logger: The logger for this class.
    """
    def __init__(self):
        # Get the logger
        self.logger: logging.Logger = logging.getLogger("algos.io.ReadStdIn")

    def integer(self) -> int:
        """
        Reads an integer from :code:`stdin`. This function expects a single line of input with only an integer present.
        If the input value is not an integer, the program raises an error.

        :raises ValueError: If the string is not a recognizable integer.
        :rtype: int
        :return: The integer held in the :code:`stdin` buffer.
        """
        # Initialize storage.
        value: int = 0
    
        # Read the line first.
        stdin_input_str: Union[str, bytes] = sys.stdin.readline()
    
        # The function is expecting a single integer input. We must handle the case where the input is a single integer.
        try:
            # The input was a recognizable integer.
            value = int(stdin_input_str)
        except ValueError as err:
            # The input was not a recognizable integer. Log the error and raise exception.
            self.logger.critical(
                "integer - " + str(err) +
                "\nInput: " + convert_anystr(stdin_input_str)
            )
            raise ValueError(err)

        return value
    
    def array(self, typ: str) -> list[Any]:
        """
        Reads in an array of a given type from :code:`stdin`. If the elements within :code:`stdin` are not all of the
        correct type, the program exits.
    
        :param str typ: The type of the elements of the list.
        :rtype: list[Any]
        :return: A list created from the :code:`stdin` input line.
        """
        # Initialize storage.
        if typ == "int" or typ == "float" or typ == "str":
            array: Union[list[int], list[float], list[str]]
        else:
            self.logger.critical("self.array - Unsupported Type\nInput " + str(typ))
            raise ValueError("Unsupported Type")
    
        # Read the line.
        stdin_input_str: Union[str, bytes] = sys.stdin.readline()
    
        # We attempt to map the input to a list of appropriate type.
        try:
            # All the entries in the input line were of the correct type.
            if typ == "int":
                array = list(map(int, stdin_input_str.split()))
            elif typ == "float":
                array = list(map(float, stdin_input_str.split()))
            if typ == "str":
                array = list(map(str, stdin_input_str.split()))
    
        except ValueError as err:
            # At least one of the entries in the input line was of an incorrect type. We log the error message and
            # raise ValueError
            self.logger.critical(
                "self.array - " + str(err) +
                "\nInput: " + convert_anystr(stdin_input_str)
            )
            raise ValueError(err)
    
        return array

    def matrix(self, n: int) -> list[list[int]]:
        """
        Reads an :math:`n*n` matrix from stdin. The input is expected to consist solely of integers.
    
        :param int n: The dimension of the square matrix.
        :rtype: list[list[int]]
        :return: A list of lists of integers representing the matrix.
        """
        # Create the list to store the results.
        M: list = []
    
        # For each line of input from stdin.
        for lines in range(n):
            # Read in the values as an array.
            row: list[int] = self.array("int")
    
            # Check that the length of the row is equal to n.
            assert len(row) == n
    
            # Append the row to storage.
            M.append(row)
    
        return M
