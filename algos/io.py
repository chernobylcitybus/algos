"""
A general module that contains a variety of helper classes supporting input/output operations. The classes
supported thus far are

+-------------------------------------+----------------------------------------------------------------------------+
| class                               | purpose                                                                    |
+=====================================+============================================================================+
| :class:`.StdIn`                     | Reads input from ``stdin`` in a variety of formats.                        |
+-------------------------------------+----------------------------------------------------------------------------+
| :class:`.ShMem`                     | Reads and writes to shared memory.                                         |
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


class StdIn:
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
        self.logger: logging.Logger = logging.getLogger("algos.io.StdIn")

    def integer(self) -> int:
        """
        Reads an integer from :code:`stdin`. This function expects a single line of input with only an integer present.
        If the input value is not an integer, the program raises an error.

        With an interactive Python session, you can run

        >>> from algos.io import StdIn
        >>> reader = StdIn()
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

        >>> from algos.io import StdIn
        >>> reader = StdIn()
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

        >>> from algos.io import StdIn
        >>> reader = StdIn()
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

        >>> from algos.io import StdIn
        >>> reader = StdIn()
        >>> reader.string()
        hello world
        how are you
        ['hello world', 'how are you', '']

        :return: The lines read in from ``stdin`` as a list.
        """
        a: list[str] = "".join(sys.stdin.readlines()).split("\n")

        return a


class ShMem:
    """
    A class that writes data to shared memory. This output can then be accessed by other processes. This is useful when
    chaining command line programs together, in order to alleviate the need to do textual processing for each
    input/output from each program in the chained command line.

    :ivar str shm_namespace: The name of the object in shared memory where the handles of the allocated objects reside.
    :ivar .SharedMemory sm_index: A region of shared memory that allows us to keep track of our allocated objects.
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
            sm_index: bytes = pickle.dumps({shm_namespace})

            # Get the length of the bytes object so that we may perform a copy.
            n_sm_index: int = len(sm_index)

            # Create the shared memory region with the same size as the pickled index.
            self.sm_index = shared_memory.SharedMemory(create=True, size=sys.getsizeof(sm_index), name=shm_namespace)

            # Perform a copy of the data to the buffer.
            self.sm_index.buf[:n_sm_index] = sm_index[:n_sm_index]

    def read_index(self) -> set[str]:
        """
        Reads the current index of the shared memory namespace. This should contain handles to all shared memory
        objects within the namespace.

        :rtype: set[str]
        :return: Shared Memory handles as strings.
        """
        return pickle.loads(bytes(self.sm_index.buf))

    def write_index(self, index: set[str]) -> None:
        """
        Writes an index, which should represent the list of shared memory object handles, to the shared memory
        namespace. Since the previously allocated space is not mutable, we have to deallocate the previous object and
        then reallocate the :attr:`.ShMem.sm_index` instance variable.

        :param set[str] index: A set of names which are handles to objects in shared memory.
        """
        # Delete the previous index.
        self.sm_index.close()
        self.sm_index.unlink()

        # Write the index to binary representation.
        sm_index: bytes = pickle.dumps(index)

        # Get the length of the bytes object so that we may perform a copy.
        n_sm_index: int = len(sm_index)

        # Create the shared memory region with the same size as the pickled index.
        self.sm_index = shared_memory.SharedMemory(create=True, size=sys.getsizeof(sm_index), name=self.shm_namespace)

        # Perform a copy of the data to the buffer.
        self.sm_index.buf[:n_sm_index] = sm_index[:n_sm_index]

    def append_index(self, index: str):
        """
        Appends a shared memory object handle onto the existing index. This does not actually append to the old
        shared memory object, but rather deallocates the old one and allocates a new shared memory object for the
        new index.

        :param str index: The shared memory object handle to add.
        """
        # Get the old index.
        old_index: set[str] = self.read_index()

        # Add the new index to the old index.
        old_index.add(index)

        # Write the updated index.
        self.write_index(old_index)

    def write(self, index: str, obj: Any):
        """
        Serializes object ``obj`` by pickling and writes to shared memory object with handle ``index``.

        :raises TypeError: If the input object cannot be pickled.
        :raises FileExistsError: If the handle has already been allocated.
        :param str index: The string handle for the shared memory object.
        :param Any obj: The object to write to shared memory. Can be any object as long as it is serializable with
                        :mod:`pickle`
        """
        # We try to pickle the object
        try:
            # Get binary representation of pickled data.
            obj_pickle: bytes = pickle.dumps(obj)
        # Otherwise the object can't be pickled
        except TypeError:
            # Raise a TypeError indicating that we were unable to pickle.
            raise TypeError("Input object cannot be pickled")

        # Get the length of the bytes object so that we may perform a copy.
        n_sm_obj: int = len(obj_pickle)

        # We try to allocate shared memory of the correct size to the desired string handle.
        # If we succeed
        try:
            # Create the shared memory region with the same size as the pickled object.
            sm_object: shared_memory.SharedMemory = shared_memory.SharedMemory(
                create=True, size=sys.getsizeof(obj_pickle), name=self.shm_namespace + "_" + index
            )
        # The shared memory handle already exists
        except FileExistsError:
            # Raise an exception with the already allocated index.
            raise FileExistsError("The shared memory handle has already been used: " + index)

        # Perform a copy of the data to the buffer.
        sm_object.buf[:n_sm_obj] = obj_pickle[:n_sm_obj]

        # Append the new index to the old index.
        self.append_index(index)

    def read(self, handle: str) -> Any:
        """
        Reads an item from shared memory with the given handle.

        :raises TypeError: If handle is not a string.
        :raises ValueError: If the handle is not located in the index.
        :param str handle: The string name of the region of shared memory.
        :rtype: Any
        :return: An unpickled copy of the object referred to by ``handle``.
        """
        # Check that the handle was given as a string.
        if not isinstance(handle, str):
            raise TypeError("Handle is not a valid string")

        # Get the current index.
        index: set[str] = self.read_index()

        # Check if the handle has been allocated and raise if it wasn't.
        if handle not in index:
            raise ValueError("Handle " + handle + " has not been allocated within namespace " + self.shm_namespace)

        # Get a memoryview of the object.
        sm_object: shared_memory.SharedMemory = shared_memory.SharedMemory(self.shm_namespace + "_" + handle)

        # Unpickle the data
        data: Any = pickle.loads(bytes(sm_object.buf))

        # Cleanup the handle to the shared memory object.
        sm_object.close()

        # Return the unpickled data.
        return data

    def delete(self, handle: str) -> None:
        """
        Deletes an item from shared memory with the given handle.

        :raises TypeError: If handle is not a string.
        :raises ValueError: If the handle is not located in the index.
        :param str handle: The string name of the region of shared memory.
        """
        # Check that the handle was given as a string.
        if not isinstance(handle, str):
            raise TypeError("Handle is not a valid string")

        # Get the current index.
        index: set[str] = self.read_index()

        # Check if the handle has been allocated and raise if it wasn't.
        if handle not in index:
            raise ValueError("Handle " + handle + " has not been allocated within namespace " + self.shm_namespace)

        # Get a memoryview of the object.
        sm_object: shared_memory.SharedMemory = shared_memory.SharedMemory(self.shm_namespace + "_" + handle)

        # Close and unlink the object.
        sm_object.close()
        sm_object.unlink()

        # Delete the object from the index.
        index.remove(handle)

        # Write the updated index.
        self.write_index(index)

    def update(self, handle: str, obj: Any) -> None:
        """
        Updates an item in shared memory with the given handle. This effectively deletes the old shared memory object,
        and writes the new shared memory object, using the same handle.

        :raises TypeError: If handle is not a string.
        :raises ValueError: If the handle is not located in the index.
        :param str handle: An existing string handle to the shared memory object.
        :param Any obj: The object to point to with the new handle, to be written to shared memory.
        """
        # Check that the handle was given as a string.
        if not isinstance(handle, str):
            raise TypeError("Handle is not a valid string")

        # Get the current index.
        index: set[str] = self.read_index()

        # Check if the handle has been allocated and raise if it wasn't.
        if handle not in index:
            raise ValueError("Handle " + handle + " has not been allocated within namespace " + self.shm_namespace)

        # Delete the object pointed to by handle in shared memory, and remove from namespace.
        self.delete(handle)

        # Write the new object to shared memory and update the namespace with the handle.
        self.write(handle, obj)
