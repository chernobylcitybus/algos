"""
A general module that contains a variety of helper classes supporting input/output operations. The classes
supported thus far are

+-------------------------------------+----------------------------------------------------------------------------+
| class                               | purpose                                                                    |
+=====================================+============================================================================+
| :class:`.ReadStdIn`                 | Reads input from ``stdin`` in a variety of formats.                        |
+-------------------------------------+----------------------------------------------------------------------------+

"""
import sys
import logging
import pickle
from typing import TypeVar, Any, Union
from multiprocessing import shared_memory


# Set up the logger for the module
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s [%(lineno)d] %(message)s "
)

NumArrTypes = TypeVar("NumArrTypes", list[int], list[float])
"""Generic variable for numeric arrays. Supports arrays that are of :class:`int` or :class:`float` ."""

NumMatTypes = TypeVar("NumMatTypes", list[list[int]], list[list[float]])
"""Generic variable for numeric matrices. Supports matrices that are of :class:`int` or :class:`float` ."""


def convert_anystr(any_str: Union[str, bytes]) -> str:
    """
    Helper function to take an :class:`.Union[str, bytes]` type and return :class:`str` output. Returns :class:`str`
    input unmodified but decodes :class:`bytes` input to :class:`str`.

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
    A class that has multiple methods for reading ``stdin`` inputs. This primarily makes it easier to handle programs
    that read from ``stdin`` such as :any:`cli` .

    :ivar logging.Logger logger: The logger for this class.
    """
    def __init__(self):
        """
        Initialize the logger for the class.
        """
        # Get the logger
        self.logger: logging.Logger = logging.getLogger("algos.io.ReadStdIn")

    def integer(self) -> int:
        """
        Reads an integer from :code:`stdin`. This function expects a single line of input with only an integer present.
        If the input value is not an integer, the program raises an error.

        With an interactive Python session, you can run

        >>> from algos.io import ReadStdIn
        >>> reader = ReadStdIn()
        >>> reader.integer()
        7
        7

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
        correct type, the program raises an exception.

        With an interactive Python session, you can run

        >>> from algos.io import ReadStdIn
        >>> reader = ReadStdIn()
        >>> reader.array("int")
        1 2 3
        [1, 2, 3]
        >>> reader.array("float")
        1.0 2.0 3.0
        [1.0, 2.0, 3.0]
        >>> reader.array("float")
        1 2.0 3
        [1.0, 2.0, 3.0]
        >>> reader.array("str")
        hello world
        ['hello', 'world']

        :raises ValueError: If the typ argument is not a supported type.
        :raises ValueError: If the inputs are unsuccessful in mapping to the given type.
        :param str typ: The type of the elements of the list.
        :rtype: list[Any]
        :return: A list created from the :code:`stdin` input line.
        """
        # Check that typ input is a string
        if not isinstance(typ, str):
            self.logger.critical("array - Unsupported Input Type\nInput " + str(type(typ)))
            raise TypeError("array - Unsupported Input Type: - " + str(type(typ)))

        # Initialize storage.
        if typ == "int" or typ == "float" or typ == "str":
            array: Union[list[int], list[float], list[str]]
        else:
            self.logger.critical("array - Unsupported Type\nInput " + typ)
            raise ValueError("Unsupported Type")
    
        # Read the line.
        stdin_input_str: Union[str, bytes] = sys.stdin.readline()

        # Handle the case of empty input.
        if stdin_input_str == "":
            raise ValueError("Empty input")
    
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
            # raise ValueError.
            self.logger.critical(
                "array - " + str(err) +
                "\nInput: " + convert_anystr(stdin_input_str)
            )
            raise ValueError(err)
    
        return array

    def matrix(self, n: int) -> list[list[int]]:
        """
        Reads an :math:`n*n` matrix from stdin. The input is expected to consist solely of integers. Only reads
        square matrices.

        With an interactive Python session, you can run

        >>> from algos.io import ReadStdIn
        >>> reader = ReadStdIn()
        >>> reader.matrix(3)
        1 2 3
        4 5 6
        7 8 9
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        >>> reader.matrix(4)
        1 2 3 4
        5 6 7 8
        1 2 3 4
        5 6 7 8
        [[1, 2, 3, 4], [5, 6, 7, 8], [1, 2, 3, 4], [5, 6, 7, 8]]


        :raises TypeError: If the number of lines to read is not an integer.
        :raises ValueError: If n is less than 1.
        :raises ValueError: If the lengths of the rows are not equal to n.
        :param int n: The dimension of the square matrix.
        :rtype: list[list[int]]
        :return: A list of lists of integers representing the matrix.
        """
        # Check that the input type of n is correct:
        if not isinstance(n, int):
            self.logger.critical("matrix - Unsupported Input Type\nInput " + str(type(n)))
            raise TypeError("matrix - Invalid Input Type: " + str(type(n)))

        # Check that n is valid
        if n < 1:
            self.logger.critical(
                "matrix - invalid n specified: " + str(n)
            )
            raise ValueError("Invalid value for n")

        # Create the list to store the results.
        M: list = []
    
        # For each line of input from stdin.
        for lines in range(n):
            # Read in the values as an array.
            row: list[int] = self.array("int")
    
            # Check that the length of the row is equal to n. If it is not, log error and raise ValueError.
            if len(row) != n:
                self.logger.critical(
                    "matrix - input row not of length " + str(n) +
                    "\nInput: " + repr(row)
                )
                raise ValueError("Row lengths not equal")
    
            # Append the row to storage.
            M.append(row)
    
        return M

    @staticmethod
    def string() -> list[str]:
        """
        Reads all the lines contained within ``stdin`` as a string and yields each line as an element of a list. The
        expected input can be anything, but reads the entirety of ``stdin``.

        In an interactive, Python session, you can use ^D (CTRL+D) to yield an EOF marker.

        >>> from algos.io import ReadStdIn
        >>> reader = ReadStdIn()
        >>> reader.string()
        hello world
        how are you
        ['hello world', 'how are you', '']

        :return: The lines read in from ``stdin`` as a list.
        """
        a: list[str] = "".join(sys.stdin.readlines()).split("\n")

        return a


class WriteShMem:
    """
    A class that writes data to shared memory. This output can then be accessed by other processes. This is useful when
    chaining command line programs together, in order to alleviate the need to do textual processing for each
    input/output from each program in the chained command line.

    :ivar shm_namespace
    :ivar sm_index: A region of shared memory that allows us to keep track of our allocated objects.
    """
    def __init__(self, shm_namespace: str):
        """
        Initializes the shared memory reader. Checks if the shared memory namespace specified exists and
        if it does not, creates an empty index to keep track of all allocated objects. The shared memory index,
        named ``shm_namespace``, is present to ensure allocated objects can be cleaned up at the end of
        processing.
        """
        # Store namespace name for later use.
        self.shm_namespace: str = shm_namespace

        # Declare the type of the shared memory index.
        self.sm_index: shared_memory.SharedMemory

        # If the index already exists
        try:
            # Attach to the shared memory object.
            self.sm_index = shared_memory.SharedMemory(shm_namespace)
        # Otherwise, the shared memory index has not been allocated
        except FileNotFoundError:
            # Create the index. We pickle in order to write to binary.
            sm_index: bytes = pickle.dumps([shm_namespace])

            # Get the length of the bytes object so that we may perform a copy.
            n_sm_index: int = len(sm_index)

            # Create the shared memory region with the same size as the pickled index.
            self.sm_index = shared_memory.SharedMemory(create=True, size=sys.getsizeof(sm_index), name=shm_namespace)

            # Perform a copy of the data to the buffer.
            self.sm_index.buf[:n_sm_index] = sm_index[:n_sm_index]
