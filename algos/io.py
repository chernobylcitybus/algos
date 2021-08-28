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
import os.path
import sys
import logging
import pickle
import tempfile
import mmap
from typing import TypeVar, Any, Union, Optional, BinaryIO
from multiprocessing import shared_memory
from pathlib import Path

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
    A class that reads and writes data from and to shared memory. This output can then be accessed by other processes.
    This is useful when chaining command line programs together, in order to alleviate the need to do textual processing
    for each input/output from each program in the chained command line. This class acts as a sort of shared memory
    manager that allows allocation of shared memory objects within a particular namespace (prefix) which is applied
    to the object's shared memory string handle. Since all objects are tracked across processes, this allows us to
    deallocate all objects and prevent memory leaks.

    On Windows it appears as if the index gets allocated correctly using :class:`.shared_memory.SharedMemory`, however,
    subsequent writes do not seem to get processed. We emulate the behaviour of the :class:`.shared_memory.SharedMemory`
    by using :mod:`mmap` on Windows. This will write the file handles to a temporary directory and create the required
    memory mapped region. In the constructor, we can choose whether to use :mod:`mmap` or
    :class:`.shared_memory.SharedMemory`. Default is :class:`.shared_memory.SharedMemory`.

    :ivar str shm_namespace: The name of the object in shared memory where the handles of the allocated objects reside.
    :ivar str mem_type: Either one of "shm" or "mmap". Determines which type of shared memory we are using.
                        Defaults to "shm" which represents :class:`.shared_memory.SharedMemory`. When equal to
                        "mmap" uses :mod:`mmap`.
    :ivar Optional[.SharedMemory] sm_index: A region of shared memory that allows us to keep track of our allocated
                                            objects when using :class:`.shared_memory.SharedMemory`.
    :ivar Optional[mmap.mmap] mm_index: A region of shared memory that allows us to keep track of our allocated objects
                                        when using
                                        :class:`mmap.mmap`.
    :ivar Optional[str] index_dir: The temporary directory where memory mapped file handles are held.
    """
    def __init__(self, shm_namespace: str, mem_type: str = "shm"):
        """
        Initializes the shared memory reader. Checks if the shared memory namespace specified exists and
        if it does not, creates an empty index to keep track of all allocated objects. The shared memory index,
        named ``shm_namespace``, is present to ensure allocated objects can be cleaned up at the end of
        processing.

        :param str shm_namespace: The name of the object in shared memory where the handles of the allocated objects
                                  reside.
        :param str mem_type: Either one of "shm" or "mmap". Determines which type of shared memory we are using.
                             Defaults to "shm" which represents :class:`.shared_memory.SharedMemory`. When equal to
                             "mmap" uses :mod:`mmap`.
        """
        # Verify that the types of our inputs are correct.
        if not isinstance(shm_namespace, str):
            raise TypeError("Incorrect type for shm_namespace: " + str(type(shm_namespace)))

        if not isinstance(mem_type, str):
            raise TypeError("Incorrect type for mem_type: " + str(type(mem_type)))

        # Check that we received a valid value for mem_type.
        if mem_type not in ["shm", "mmap"]:
            raise ValueError("Incorrect value specified for mem_type: " + mem_type)

        # Store namespace name for later use.
        self.shm_namespace: Optional[str] = shm_namespace

        # Store the memory type for later use.
        self.mem_type: str = mem_type

        # Declare the type of the shared memory index and initialize.
        self.sm_index: Optional[shared_memory.SharedMemory] = None

        # Declare the memory map index and initialize.
        self.mm_index: Optional[mmap.mmap] = None

        # Declare index_dir for mmap.
        index_dir: Optional[str] = None

        # If we are using multiprocessing shared memory
        if self.mem_type == "shm":
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
                self.sm_index = shared_memory.SharedMemory(
                    create=True,
                    size=sys.getsizeof(sm_index),
                    name=shm_namespace
                )

                # Perform a copy of the data to the buffer.
                self.sm_index.buf[:n_sm_index] = sm_index[:n_sm_index]

        # Otherwise we are using mmap
        else:
            # Declare a file descriptor to use for memory map.
            fd: BinaryIO

            # Get the path to the index. We use the path to the temp directory as returned by gettempdir().
            # We append the namespace and the word "index" to that to have a directory for all the memory mapped
            # files, with the index represented by the file named "mmap_index"
            index_dir = os.path.join(tempfile.gettempdir(), self.shm_namespace)
            index_path: str = os.path.join(index_dir, "mmap_index")

            # Assign the index directory to an instance variable for later use.
            self.index_dir = index_dir

            # Create the parent namespace directory if it does not exist.
            if not os.path.exists(index_dir):
                Path(index_dir).mkdir(parents=True)

            # If the index already exists:
            if os.path.exists(index_path):
                # Open the index and attach a mmap instance to the file.
                fd = open(index_path, "r+b")
                self.mm_index = mmap.mmap(fd.fileno(), 0)

                # Close the file descriptor to free up resources.
                fd.close()

            # Otherwise the memory map index has not been created.
            else:
                # Open the file for reading and writing.
                fd = open(index_path, "w+b")

                # Zero out the file as we cannot memory map an empty file.
                assert fd.write(b"\x00" * 1024) == 1024

                # Flush the changes to disk.
                fd.flush()

                # Map the file to the index.
                self.mm_index = mmap.mmap(fd.fileno(), 0)

                # Close the file descriptor to free up resources.
                fd.close()

                # Create the initial index
                init_index: bytes = pickle.dumps({shm_namespace})

                # Resize the memory mapped file for the new data
                self.mm_index.resize(sys.getsizeof(init_index))

                # Write the first index entry to the memory mapped file.
                self.mm_index.write(init_index)

                # Make sure the data is flushed.
                self.mm_index.flush()

                # Seek back to the beginning of the file for the next operation.
                self.mm_index.seek(os.SEEK_SET)

    def read_index(self) -> set[str]:
        """
        Reads the current index of the shared memory namespace. This should contain handles to all shared memory
        objects within the namespace. As an example, we can look at the index after the manager has been initialized.

        >>> from algos.io import ShMem
        >>> sm_manager = ShMem("test")
        >>> sm_manager.read_index()
        {'test'}

        :rtype: set[str]
        :return: Shared Memory handles as strings.
        """
        # Check that the manager hasn't been deallocated already.
        self.check_self()

        # If we are using multiprocessing shared memory
        if self.mem_type == "shm":
            # Return the index from the sm_index buffer.
            return pickle.loads(bytes(self.sm_index.buf))

        # Otherwise we are using mmap
        else:
            # Read the data in the memory mapped file.
            index: set[str] = pickle.loads(self.mm_index.read())

            # Reset the file pointer for the next operation.
            self.mm_index.seek(os.SEEK_SET)

            return index

    def write_index(self, index: set[str]) -> None:
        """
        Writes an index, which should represent the list of shared memory object handles, to the shared memory
        namespace. Since the previously allocated space is not mutable, we have to deallocate the previous object and
        then reallocate the :attr:`.ShMem.sm_index` instance variable. This function should not be used directly.

        :param set[str] index: A set of names which are handles to objects in shared memory.
        """
        # Check that the manager hasn't been deallocated already.
        self.check_self()

        # If we are using multiprocessing shared memory
        if self.mem_type == "shm":
            # Delete the previous index.
            self.sm_index.close()
            self.sm_index.unlink()

            # Write the index to binary representation.
            sm_index: bytes = pickle.dumps(index)

            # Get the length of the bytes object so that we may perform a copy.
            n_sm_index: int = len(sm_index)

            # Create the shared memory region with the same size as the pickled index.
            self.sm_index = shared_memory.SharedMemory(
                create=True,
                size=sys.getsizeof(sm_index),
                name=self.shm_namespace
            )

            # Perform a copy of the data to the buffer.
            self.sm_index.buf[:n_sm_index] = sm_index[:n_sm_index]
        # Otherwise we are using mmap
        else:
            # Create the initial index.
            index_pickle: bytes = pickle.dumps(index)

            # Resize the memory mapped file for the new data.
            self.mm_index.resize(sys.getsizeof(index_pickle))

            # Write the first index entry to the memory mapped file.
            self.mm_index.write(index_pickle)

            # Make sure the data is flushed.
            self.mm_index.flush()

            # Seek back to the beginning of the file for the next operation.
            self.mm_index.seek(os.SEEK_SET)

    def append_index(self, index: str):
        """
        Appends a shared memory object handle onto the existing index. This does not actually append to the old
        shared memory object, but rather deallocates the old one and allocates a new shared memory object for the
        new index. This function should not be used directly.

        :param str index: The shared memory object handle to add.
        """
        # Check that the manager hasn't been deallocated already.
        self.check_self()

        # Get the old index.
        old_index: set[str] = self.read_index()

        # Add the new index to the old index.
        old_index.add(index)

        # Write the updated index.
        self.write_index(old_index)

    def write(self, index: str, obj: Any):
        """
        Serializes object ``obj`` by pickling and writes to shared memory object with handle ``index``. We can
        add an object to shared memory as follows:

        >>> from algos.io import ShMem
        >>> sm_manager = ShMem("test")
        >>> sm_manager.write("new_data", [1, 2, 3])
        >>> sm_manager.read("new_data")
        [1, 2, 3]

        :raises TypeError: If the input object cannot be pickled.
        :raises FileExistsError: If the handle has already been allocated.
        :param str index: The string handle for the shared memory object.
        :param Any obj: The object to write to shared memory. Can be any object as long as it is serializable with
                        :mod:`pickle`
        """
        # Check that the manager hasn't been deallocated already.
        self.check_self()

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

        # If we are using multiprocessing shared memory
        if self.mem_type == "shm":
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

        # Otherwise we are using mmap
        else:
            # We check if the file exists.
            if os.path.exists(os.path.join(self.index_dir, index)):
                raise FileExistsError("The shared memory handle has already been used: " + index)

            # Open the file for reading and writing.
            fd = open(os.path.join(self.index_dir, index), "w+b")

            # Zero out the file as we cannot memory map an empty file.
            assert fd.write(b"\x00" * 1024) == 1024

            # Flush the changes to disk.
            fd.flush()

            # Seek to the beginning of the file.
            fd.seek(os.SEEK_SET)

            # Map the file to the index.
            mmap_handle = mmap.mmap(fd.fileno(), 0)

            # Close the file descriptor to free up resources.
            fd.close()

            # Pickle the object to write to the memory region.
            pickled_data: bytes = pickle.dumps(obj)

            # Resize the memory mapped file for the new data.
            mmap_handle.resize(sys.getsizeof(pickled_data))

            # Write the data to the memory mapped file.
            mmap_handle.write(pickled_data)

            # Make sure the data is flushed.
            mmap_handle.flush()

            # Seek back to the beginning of the file for the next operation.
            mmap_handle.seek(os.SEEK_SET)

        # Append the new index to the old index.
        self.append_index(index)

    def read(self, handle: str) -> Any:
        """
        Reads an item from shared memory with the given handle. This example is identical to the one for the write
        method

        >>> from algos.io import ShMem
        >>> sm_manager = ShMem("test")
        >>> sm_manager.write("new_data", [1, 2, 3])
        >>> sm_manager.read("new_data")
        [1, 2, 3]

        :raises TypeError: If handle is not a string.
        :raises ValueError: If the handle is not located in the index.
        :param str handle: The string name of the region of shared memory.
        :rtype: Any
        :return: An unpickled copy of the object referred to by ``handle``.
        """
        # Check that the manager hasn't been deallocated already.
        self.check_self()

        # Check that the handle was given as a string.
        if not isinstance(handle, str):
            raise TypeError("Handle is not a valid string")

        # Get the current index.
        index: set[str] = self.read_index()

        # Check if the handle has been allocated and raise if it wasn't.
        if handle not in index:
            raise ValueError("Handle " + handle + " has not been allocated within namespace " + self.shm_namespace)

        # Declare the type of the data as Any (since it can be anything)
        data: Any

        # Declare a memory map handle if we are using mmap.
        mmap_handle: Optional[mmap.mmap] = None

        # If we are using multiprocessing shared memory
        if self.mem_type == "shm":
            # Get a memoryview of the object.
            sm_object: shared_memory.SharedMemory = shared_memory.SharedMemory(self.shm_namespace + "_" + handle)

            # Unpickle the data.
            data = pickle.loads(bytes(sm_object.buf))

            # Cleanup the handle to the shared memory object.
            sm_object.close()

        # Otherwise we are using mmap
        else:
            # Open the file for reading and writing.
            fd = open(os.path.join(self.index_dir, handle), "r+b")

            # Map the file to the index.
            mmap_handle = mmap.mmap(fd.fileno(), 0)

            # Close the file descriptor to free up resources.
            fd.close()

            # Unpickle the data
            data = pickle.loads(mmap_handle.read())

        # Return the unpickled data.
        return data

    def delete(self, handle: str) -> None:
        """
        Deletes an item from shared memory with the given handle. As a continuation of the above example:

        >>> from algos.io import ShMem
        >>> sm_manager = ShMem("test")
        >>> sm_manager.write("new_data", [1, 2, 3])
        >>> sm_manager.read("new_data")
        [1, 2, 3]
        >>> sm_manager.delete("new_data")
        >>> sm_manager.read("new_data")
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "/home/user/Documents/algos/algos/io.py", line 408, in read
            >>> sm_manager.write("new_data", [1, 2, 3])
        ValueError: Handle new_data has not been allocated within namespace test

        :raises TypeError: If handle is not a string.
        :raises ValueError: If the handle is not located in the index.
        :param str handle: The string name of the region of shared memory.
        """
        # Check that the manager hasn't been deallocated already.
        self.check_self()

        # Check that the handle was given as a string.
        if not isinstance(handle, str):
            raise TypeError("Handle is not a valid string")

        # Get the current index.
        index: set[str] = self.read_index()

        # Check if the handle has been allocated and raise if it wasn't.
        if handle not in index:
            raise ValueError("Handle " + handle + " has not been allocated within namespace " + self.shm_namespace)

        # If we are using multiprocessing shared memory
        if self.mem_type == "shm":
            # Get a memoryview of the object.
            sm_object: shared_memory.SharedMemory = shared_memory.SharedMemory(self.shm_namespace + "_" + handle)

            # Close and unlink the object.
            sm_object.close()
            sm_object.unlink()

        # Otherwise we are using mmap
        else:
            # Open the file for reading and writing.
            fd = open(os.path.join(self.index_dir, handle), "r+b")

            # Map the file to the index.
            mmap_handle = mmap.mmap(fd.fileno(), 0)

            # Close the mmap handle.
            mmap_handle.close()

            # Close the file descriptor.
            fd.close()

            # Delete the file handle from the file system.
            os.unlink(os.path.join(self.index_dir, handle))

        # Delete the object from the index.
        index.remove(handle)

        # Write the updated index.
        self.write_index(index)

    def update(self, handle: str, obj: Any) -> None:
        """
        Updates an item in shared memory with the given handle. This effectively deletes the old shared memory object,
        and writes the new shared memory object, using the same handle. To update an item, we can do the following

        >>> from algos.io import ShMem
        >>> sm_manager = ShMem("test")
        >>> sm_manager.write("new_data", ["a", "b", "c"])
        >>> sm_manager.read("new_data")
        ['a', 'b', 'c']
        >>> sm_manager.update("new_data", [1, 2, 3])
        >>> sm_manager.read("new_data")
        [1, 2, 3]

        :raises TypeError: If handle is not a string.
        :raises ValueError: If the handle is not located in the index.
        :param str handle: An existing string handle to the shared memory object.
        :param Any obj: The object to point to with the new handle, to be written to shared memory.
        """
        # Check that the manager hasn't been deallocated already.
        self.check_self()

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

    def erase(self):
        """
        Deallocates all shared memory objects and the index for this shared memory manager's
        :attr:`ShMem.shm_namespace`. Used for cleanup, once we are finished with all our objects.

        >>> from algos.io import ShMem
        >>> sm_manager = ShMem("test")
        >>> sm_manager.write("new_data", ["a", "b", "c"])
        >>> sm_manager.read("new_data")
        ['a', 'b', 'c']
        >>> sm_manager.erase()
        """
        # Check that the manager hasn't been deallocated already.
        self.check_self()

        # Get the set of all allocated objects' handles.
        index: set[str] = self.read_index()

        # Remove the name of the namespace from the index.
        index.remove(self.shm_namespace)

        # Iterate over all the handles, deleting the objects as we go along.
        handle: str
        for handle in index:
            self.delete(handle)

        if self.mem_type == "shm":
            # Remove the index.
            self.sm_index.close()
            self.sm_index.unlink()
        else:
            # Close the memory mapped file.
            self.mm_index.close()

            # Delete the file handle from the filesystem.
            os.unlink(os.path.join(self.index_dir, "mmap_index"))

            # Delete the index directory also.
            os.rmdir(self.index_dir)

        # Delete the instance variables.
        del self.sm_index
        del self.shm_namespace
        del self.mm_index

    def check_self(self):
        """
        See if this object has not already been deallocated. Used to guard function calls in case :meth:`ShMem.erase`
        has already been called.

        :raises RuntimeError: If the manager has already been erased.
        """
        try:
            self.shm_namespace
        except AttributeError:
            raise RuntimeError("Manager has already been deallocated")
