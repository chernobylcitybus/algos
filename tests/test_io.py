"""
The test module for :mod:`algos.io` . Consists of various data classes such as :class:`DataStdIn` that stores
expected inputs and outputs for the different input/output algorithms. The classes also provides data for exception
handling tests.

Each class in :mod:`algos.io` is mapped to an equivalently named test class for the purpose of these tests.
"""
import io
import sys
import re
import pickle
import pytest
from multiprocessing import shared_memory
from concurrent import futures
from algos.io import StdIn, ShMem, convert_anystr


def test_convert_anystr():
    """
    Tests cases for :func:`.convert_anystr`. Checks that both string and bytes input convert to string.

    +--------------------------------------+----------------------------------------------------------------------+
    | description                          | reason                                                               |
    +======================================+======================================================================+
    | :class:`str` input                   | Check that the function returns the string input.                    |
    +--------------------------------------+----------------------------------------------------------------------+
    | :class:`bytes` input                 | Check that the function returns a string value for bytes input       |
    +--------------------------------------+----------------------------------------------------------------------+

    """

    assert isinstance(convert_anystr("hello"), str)
    assert isinstance(convert_anystr(b"hello"), str)


class DataStdIn:
    """
    Holds the data for :class:`.StdIn` .
    """
    integer__expected = [
        ("1", 1),
        ("-1", -1),
        ("0", 0),
        ("1000000000000000000000", 1000000000000000000000)
    ]
    """
    Test cases for :meth:`.StdIn.integer`, testing that it functions correctly for expected inputs.The test
    cases are as follows
    
    +--------------------------------------+----------------------------------------------------------------------+
    | description                          | reason                                                               |
    +======================================+======================================================================+
    | read positive integer                | Check to see if an unprefixed string integer reads in correctly      |
    +--------------------------------------+----------------------------------------------------------------------+
    | read negative integer                | Check to see if reading a string number prefixed with '-' yields a   |
    |                                      | negative number.                                                     |
    +--------------------------------------+----------------------------------------------------------------------+
    | read 0                               | See if reading '0' works as expected                                 |
    +--------------------------------------+----------------------------------------------------------------------+
    | large number                         | See if large numbers are interpreted correctly.                      |
    +--------------------------------------+----------------------------------------------------------------------+
    
    """

    integer__unexpected = [
        ("a", [ValueError, "invalid literal for int() with base 10: 'a'"]),
        ("", [ValueError, "invalid literal for int() with base 10: ''"]),
        ("0.01", [ValueError, "invalid literal for int() with base 10: '0.01'"])
    ]
    """
    Test cases for :meth:`.StdIn.integer`, testing that it raises an error for unexpected inputs. The test cases
    are as follows

    +--------------------------------------+----------------------------------------------------------------------+
    | description                          | reason                                                               |
    +======================================+======================================================================+
    | read non-numeric character           | See if :class:`ValueError` is raised on non-numeric input.           |
    +--------------------------------------+----------------------------------------------------------------------+
    | read empty string                    | The function should raise :class:`ValueError` on blank input.        |
    +--------------------------------------+----------------------------------------------------------------------+
    | read float                           | The function should raise :class:`ValueError` as we are expecting    |
    |                                      | integer input.                                                       |
    +--------------------------------------+----------------------------------------------------------------------+
    
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
    Test cases for :meth:`.StdIn.array`, testing that it functions correctly for expected inputs. The test cases
    are as follows

    +--------------------------------------+----------------------------------------------------------------------+
    | description                          | reason                                                               |
    +======================================+======================================================================+
    | read integers                        | See that we get an array of integers back.                           |
    +--------------------------------------+----------------------------------------------------------------------+
    | read float                           | See that we get an array of floats back.                             |
    +--------------------------------------+----------------------------------------------------------------------+
    | read mixed floats                    | See that floats read in correctly, even without decimal notation.    |
    +--------------------------------------+----------------------------------------------------------------------+
    | read characters                      | See if characters return an array of strings.                        |
    +--------------------------------------+----------------------------------------------------------------------+
    | read numeric as characters           | See if numeric values return string if :class:`str` type specified   |
    +--------------------------------------+----------------------------------------------------------------------+
    | read words                           | See if we get an array of words back, the whitespace characters      |
    |                                      | being the delimiters                                                 |
    +--------------------------------------+----------------------------------------------------------------------+
    
    """

    array__unexpected = [
        (("int", "1 2 a"), [ValueError, "invalid literal for int() with base 10: 'a'"]),
        (("int", ""), [ValueError, "Empty input"]),
        (("int", "1 2 3.0"), [ValueError, "invalid literal for int() with base 10: '3.0'"]),
        (("float", "1 2 a"), [ValueError, "could not convert string to float: 'a'"]),
        (("hello", "a b c"), [ValueError, "Unsupported Type"]),
        ((["int"], "1 2 3"), [TypeError, "array - Unsupported Input Type: - " + str(type(list()))])
    ]
    """
    Test cases for :meth:`.StdIn.array`, testing that it raises an error for unexpected inputs. The test cases
    are as follows

    +--------------------------------------+----------------------------------------------------------------------+
    | description                          | reason                                                               |
    +======================================+======================================================================+
    | character in integer input           | Check that :class:`ValueError` is raised when input contains a non   |
    |                                      | numeric character.                                                   |
    +--------------------------------------+----------------------------------------------------------------------+
    | empty input                          | Check that :class:`ValueError` is raised when an empty input string  |
    |                                      | is given.                                                            |
    +--------------------------------------+----------------------------------------------------------------------+
    | float in integers                    | See that a :class:`ValueError` is raised if decimal notation appears |
    |                                      | when reading integers.                                               |
    +--------------------------------------+----------------------------------------------------------------------+
    | character in float                   | See that a non-numeric character raises :class:`ValueError` if       |
    |                                      | we are parsing floats.                                               |
    +--------------------------------------+----------------------------------------------------------------------+
    | invalid type string                  | Raise :class:`ValueError` if an invalid input for ``typ`` was given. |
    +--------------------------------------+----------------------------------------------------------------------+
    | invalid type for parameter           | The functions should raise :class:`TypeError` if the input parameter |
    |                                      | is not a :class:`str` .                                              |
    +--------------------------------------+----------------------------------------------------------------------+
    
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
    Test cases for :meth:`.StdIn.matrix`, testing that it functions correctly for expected inputs. The test cases
    are as follows

    +--------------------------------------+----------------------------------------------------------------------+
    | description                          | reason                                                               |
    +======================================+======================================================================+
    | 3x3                                  | Check that a 3*3 matrix reads in with three lines of correct input.  |
    +--------------------------------------+----------------------------------------------------------------------+
    | 2x2                                  | Check that a 2*2 matrix reads in with three lines of correct input.  |
    +--------------------------------------+----------------------------------------------------------------------+
    
    """

    matrix__unexpected = [
        ((2, "1 2\n4 6 7"), [ValueError, "Row lengths not equal"]),
        ((2, ""), [ValueError, "Empty input"]),
        ((0, ""), [ValueError, "Invalid value for n"]),
        ((-1, ""), [ValueError, "Invalid value for n"]),
        (([0], ""), [TypeError, "matrix - Invalid Input Type: " + str(type(list()))])
    ]
    """
    Test cases for :meth:`.StdIn.matrix`, testing that it raises an error for unexpected inputs. The test cases
    are as follows

    +--------------------------------------+----------------------------------------------------------------------+
    | description                          | reason                                                               |
    +======================================+======================================================================+
    | too many elements in row             | See that :class:`ValueError` is raised if the row lengths are off.   |
    +--------------------------------------+----------------------------------------------------------------------+
    | empty input                          | See that :class:`ValueError` is raised when an empty input string is |
    |                                      | given.                                                               |
    +--------------------------------------+----------------------------------------------------------------------+
    | read no lines                        | The function should raise :class:`ValueError` if told to read        |
    |                                      | 0 lines.                                                             |
    +--------------------------------------+----------------------------------------------------------------------+
    | read negative lines                  | The function should raise :class:`ValueError` if told to read        |
    |                                      | a negative number of  lines.                                         |
    +--------------------------------------+----------------------------------------------------------------------+
    | wrong input type for lines to read   | See if a :class:`TypeError` is raised for anything but :class:`int`. |
    +--------------------------------------+----------------------------------------------------------------------+
    
    """

    string__expected = [
        ("", [""]),
        ("abc", ["abc"]),
        ("abc\ndef", ["abc", "def"]),
        ("hello world\nhow are you?", ["hello world", "how are you?"])
    ]
    """
    Test cases for :meth:`.StdIn.string`, testing that it functions correctly for expected inputs. The test cases
    are as follows

    +--------------------------------------+----------------------------------------------------------------------+
    | description                          | reason                                                               |
    +======================================+======================================================================+
    | empty string                         | See that a list with just one empty string is returned.              |
    +--------------------------------------+----------------------------------------------------------------------+
    | read one line                        | See if a word is read in as a one element array.                     |
    +--------------------------------------+----------------------------------------------------------------------+
    | read two lines                       | See if two lines are read in as a two element array.                 |
    +--------------------------------------+----------------------------------------------------------------------+
    | read sentences                       | See if two lines of sentences is read in as a two element array.     |
    +--------------------------------------+----------------------------------------------------------------------+
    
    """


class TestStdIn:
    """
    Test cases for :class:`.StdIn`.
    """
    @pytest.mark.parametrize(
        "test_input,expected",
        DataStdIn.integer__expected,
        ids=[repr(v) for v in DataStdIn.integer__expected]
    )
    def test_integer__expected(self, monkeypatch, test_input, expected):
        """
        Test that the :meth:`.StdIn.integer` method works properly for expected inputs. Test input can be found
        in :attr:`DataStdIn.integer__expected` .

        We monkeypatch ``stdin`` to run our test cases with the mock data.
        """
        # Monkeypatch stdin to hold the value we want the program to read as input.
        monkeypatch.setattr('sys.stdin', io.StringIO(test_input))

        # Create the reader instance.
        reader = StdIn()

        # Check that the value is the same as the monkeypatched value.
        assert reader.integer() == expected

    @pytest.mark.parametrize(
        "test_input,error",
        DataStdIn.integer__unexpected,
        ids=[repr(v) for v in DataStdIn.integer__unexpected]
    )
    def test_integer__unexpected(self, monkeypatch, test_input, error):
        """
        Test that the :meth:`.StdIn.integer` raises exceptions for unexpected inputs. Test input can be found
        in :attr:`DataStdIn.integer__unexpected` .

        We monkeypatch ``stdin`` to run our test cases with the mock data. We check if the specified exception was
        raised and that the expected exception reason matches the raised exception.
        """
        # Monkeypatch stdin to hold the value we want the program to read as input.
        monkeypatch.setattr('sys.stdin', io.StringIO(test_input))

        # Create the reader instance.
        reader = StdIn()

        # Check that the exception is raised.
        with pytest.raises(error[0]) as excinfo:
            reader.integer()

        # Check that the errors match.
        assert excinfo.match(re.escape(error[1]))

    @pytest.mark.parametrize(
        "test_input,expected",
        DataStdIn.array__expected,
        ids=[repr(v) for v in DataStdIn.array__expected]
    )
    def test_array__expected(self, monkeypatch, test_input, expected):
        """
        Test that the :meth:`.StdIn.array` method works properly for expected inputs. Test input can be found
        in :attr:`DataStdIn.array__expected` .

        We monkeypatch ``stdin`` to run our test cases with the mock data.
        """
        # Reassign input array to meaningful names.
        input_type = test_input[0]
        input_str = test_input[1]

        # Monkeypatch stdin to hold the value we want the program to read as input.
        monkeypatch.setattr('sys.stdin', io.StringIO(input_str))

        # Create the reader instance.
        reader = StdIn()

        # Check that the value is the same as the monkeypatched value.
        assert reader.array(input_type) == expected

    @pytest.mark.parametrize(
        "test_input,error",
        DataStdIn.array__unexpected,
        ids=[repr(v) for v in DataStdIn.array__unexpected]
    )
    def test_array__unexpected(self, monkeypatch, test_input, error):
        """
        Test that the :meth:`.StdIn.array` raises exceptions for unexpected inputs. Test input can be found
        in :attr:`DataStdIn.array__unexpected` .

        We monkeypatch ``stdin`` to run our test cases with the mock data. We check if the specified exception was
        raised and that the expected exception reason matches the raised exception.
        """
        # Reassign input array to meaningful names.
        input_type = test_input[0]
        input_str = test_input[1]

        # Monkeypatch stdin to hold the value we want the program to read as input
        monkeypatch.setattr('sys.stdin', io.StringIO(input_str))

        # Create the reader instance.
        reader = StdIn()

        # Check that the exception is raised.
        with pytest.raises(error[0]) as excinfo:
            reader.array(input_type)

        assert excinfo.match(re.escape(error[1]))

    @pytest.mark.parametrize(
        "test_input,expected",
        DataStdIn.matrix__expected,
        ids=[repr(v) for v in DataStdIn.matrix__expected]
    )
    def test_matrix__expected(self, monkeypatch, test_input, expected):
        """
        Test that the :meth:`.StdIn.matrix` method works properly for expected inputs. Test input can be found
        in :attr:`DataStdIn.matrix__expected` .

        We monkeypatch ``stdin`` to run our test cases with the mock data.
        """
        # Reassign input array to meaningful names.
        n = test_input[0]
        input_str = test_input[1]

        # Monkeypatch stdin to hold the value we want the program to read as input.
        monkeypatch.setattr('sys.stdin', io.StringIO(input_str))

        # Create the reader instance.
        reader = StdIn()

        # Check that the value is the same as the monkeypatched value.
        assert reader.matrix(n) == expected

    @pytest.mark.parametrize(
        "test_input,error",
        DataStdIn.matrix__unexpected,
        ids=[repr(v) for v in DataStdIn.matrix__unexpected]
    )
    def test_matrix__unexpected(self, monkeypatch, test_input, error):
        """
        Test that the :meth:`.StdIn.matrix` raises exceptions for unexpected inputs. Test input can be found
        in :attr:`DataStdIn.matrix__unexpected` .

        We monkeypatch ``stdin`` to run our test cases with the mock data. We check if the specified exception was
        raised and that the expected exception reason matches the raised exception.
        """
        # Reassign input array to meaningful names.
        n = test_input[0]
        input_str = test_input[1]

        # Monkeypatch stdin to hold the value we want the program to read as input
        monkeypatch.setattr('sys.stdin', io.StringIO(input_str))

        # Create the reader instance.
        reader = StdIn()

        # Check that the exception is raised.
        with pytest.raises(error[0]) as excinfo:
            reader.matrix(n)

        assert excinfo.match(re.escape(error[1]))

    @pytest.mark.parametrize(
        "test_input,expected",
        DataStdIn.string__expected,
        ids=[repr(v) for v in DataStdIn.string__expected]
    )
    def test_string__expected(self, monkeypatch, test_input, expected):
        """
        Test that the :meth:`.StdIn.string` method works properly for expected inputs. Test input can be found
        in :attr:`DataStdIn.string__expected` .

        We monkeypatch ``stdin`` to run our test cases with the mock data.
        """
        # Monkeypatch stdin to hold the value we want the program to read as input.
        monkeypatch.setattr('sys.stdin', io.StringIO(test_input))

        # Create the reader instance.
        reader = StdIn()

        # Check that the value is the same as the monkeypatched value.
        assert reader.string() == expected


class TestShMem:
    """
    Test cases for :class:`.ShMem`.
    """
    def test_init(self):
        """
        Test the init function to see if

        +--------------------------------------+----------------------------------------------------------------------+
        | description                          | reason                                                               |
        +======================================+======================================================================+
        | no shared memory index               | Function should create one.                                          |
        +--------------------------------------+----------------------------------------------------------------------+
        | shared memory index                  | Function should attach to the index.                                 |
        +--------------------------------------+----------------------------------------------------------------------+
        """
        # Create a shared memory object. At this stage, there should be none named algoscli.
        shm_manager = ShMem("algoscli")

        # Check that we have the initial data in the buffer.
        assert pickle.loads(bytes(shm_manager.sm_index.buf)) == {"algoscli"}

        # Clean up the shared memory index.
        shm_manager.sm_index.close()
        shm_manager.sm_index.unlink()

        # Delete the shm_manager object.
        del shm_manager

        # Create the index again. We pickle in order to write to binary.
        sm_index_data: bytes = pickle.dumps({"already exists"})

        # Get the length of the bytes object so that we may perform a copy.
        n_sm_index: int = len(sm_index_data)

        # Create the shared memory region with the same size as the pickled index.
        sm_index = shared_memory.SharedMemory(create=True, size=sys.getsizeof(sm_index_data), name="algoscli")

        # Perform a copy of the data to the buffer.
        sm_index.buf[:n_sm_index] = sm_index_data[:n_sm_index]

        # Create a shared memory object. At this stage, there should be the object created above named algoscli.
        shm_manager = ShMem("algoscli")

        # Check that we have the initial data in the buffer.
        assert pickle.loads(bytes(shm_manager.sm_index.buf)) == {"already exists"}

        # Clean up the shared memory index.
        shm_manager.sm_index.close()
        shm_manager.sm_index.unlink()

    def test_read_index(self):
        """
        Test that :meth:`.ShMem.read_index` returns the correct current index for all shared memory objects
        allocated within the namespace.
        """
        # Create a shared memory object.
        shm_manager = ShMem("test")

        # Read the index.
        index = shm_manager.read_index()

        # Check that the index is as we expected.
        assert index == {"test"}

        # Clean up the shared memory region.
        shm_manager.sm_index.close()
        shm_manager.sm_index.unlink()

    def test_write_index(self):
        """
        Test that :meth:`.ShMem.write_index` correctly updates the shared memory object index. Checks that the shared
        memory buffer contains the updated index.
        """
        # Create a shared memory object.
        shm_manager = ShMem("test")

        # Read the index.
        index = shm_manager.read_index()

        # Update the namespace with the handles "a", "b" and "c".
        [index.add(x) for x in {"a", "b", "c"}]

        # Write the updated index.
        shm_manager.write_index(index)

        # Read the updated index.
        index = shm_manager.read_index()

        # Clean up the shared memory region.
        shm_manager.sm_index.close()
        shm_manager.sm_index.unlink()

        assert index == {"test", "a", "b", "c"}

    def test_append_index(self):
        """
        Test that :meth:`.ShMem.append_index` correctly appends to the shared memory object index. Checks that the
        namespace has been updated.
        """
        # Create a shared memory object.
        shm_manager = ShMem("test")

        # Append some indexes.
        shm_manager.append_index("hello")
        shm_manager.append_index("world")

        # Read the updated index.
        index = shm_manager.read_index()

        # Clean up the shared memory region.
        shm_manager.sm_index.close()
        shm_manager.sm_index.unlink()

        assert index == {"test", "hello", "world"}

    def test_write__expected(self):
        """
        Test that :meth:`.ShMem.write` correctly appends to the shared memory object index. Checks that the namespace
        has been updated, and the objects allocated to shared memory.
        """
        # Create a shared memory object.
        shm_manager = ShMem("test")

        # Write some data.
        shm_manager.write("test_names", ["Kolmogorov", "Markov", "Gauss"])

        # Read the updated index.
        index = shm_manager.read_index()

        # Read the data.
        sm_handle = shared_memory.SharedMemory("test_test_names")
        sm_data = pickle.loads(bytes(sm_handle.buf))

        # Clean up the shared memory region.
        shm_manager.sm_index.close()
        shm_manager.sm_index.unlink()
        sm_handle.close()
        sm_handle.unlink()

        assert index == {"test", "test_names"}
        assert sm_data == ['Kolmogorov', 'Markov', 'Gauss']

    def test_write__unexpected(self):
        """
        Test that the :meth:`.ShMem.write` raises an exception in the following cases

        +--------------------------------------+----------------------------------------------------------------------+
        | description                          | reason                                                               |
        +======================================+======================================================================+
        | object cannot be pickled             | See if :class:`TypeError` is raised as this data can't be shared.    |
        +--------------------------------------+----------------------------------------------------------------------+
        | shared memory already allocated      | See if :class:`FileExistsError` is raised, indicating the shared     |
        |                                      | memory handle has already been used.                                 |
        +--------------------------------------+----------------------------------------------------------------------+
        """
        # Create a shared memory object.
        shm_manager = ShMem("test")

        # Try to pickle something that cannot be pickled.
        with pytest.raises(TypeError) as excinfo:
            shm_manager.write("test_data", futures.Future())

        # Check that we have raised the correct error.
        assert excinfo.match("Input object cannot be pickled")

        # Try allocating something to a name that has already been allocated.
        shm_manager.write("test_data", "Hello")
        with pytest.raises(FileExistsError) as excinfo:
            shm_manager.write("test_data", "World")

        # Check that we raised the correct error.
        assert excinfo.match("The shared memory handle has already been used: test_data")

        # Read the data.
        sm_handle = shared_memory.SharedMemory("test_test_data")

        # Clean up the shared memory region.
        shm_manager.sm_index.close()
        shm_manager.sm_index.unlink()
        sm_handle.close()
        sm_handle.unlink()

    def test_read__expected(self):
        """
        Test that the :meth:`.ShMem.read` functions as expected for expected inputs.
        """
        # Create a shared memory object.
        shm_manager = ShMem("test")

        # Create some data.
        a = ["Kolmogorov", "Markov", "Gauss"]
        b = 42
        c = {"hello": set("world")}

        # Write some data.
        shm_manager.write("a", a)
        shm_manager.write("b", b)
        shm_manager.write("c", c)

        # Try reading the data from shared memory.
        results = [shm_manager.read(x) for x in ["a", "b", "c"]]

        # Clean up the allocated objects.
        for i in ["a", "b", "c"]:
            sm_handle = shared_memory.SharedMemory("test_" + i)
            sm_handle.close()
            sm_handle.unlink()

        # Clean up the shared memory region.
        shm_manager.sm_index.close()
        shm_manager.sm_index.unlink()

        # Check that the results are the same as the input data.
        assert results == [a, b, c]

    def test_read__unexpected(self):
        """
        Test that the :meth:`.ShMem.read` raises an exception in the following cases

        +--------------------------------------+----------------------------------------------------------------------+
        | description                          | reason                                                               |
        +======================================+======================================================================+
        | handle not a string                  | See if we raise :class:`TypeError` if handle is given as anything    |
        |                                      | but a string.                                                        |
        +--------------------------------------+----------------------------------------------------------------------+
        | handle not allocated                 | See if we raise :class:`ValueError` if handle does not exit.         |
        +--------------------------------------+----------------------------------------------------------------------+
        """
        # Create a shared memory object.
        shm_manager = ShMem("test")

        # Try to raise a TypeError by supplying a non-string handle.
        with pytest.raises(TypeError) as excinfo:
            shm_manager.read(1)

        # Check that we raised the correct exception message.
        assert excinfo.match("Handle is not a valid string")

        # Try to raise a ValueError by supplying a handle that does not exist.
        with pytest.raises(ValueError) as excinfo:
            shm_manager.read("does_not_exist")

        # See if we get the right exception.
        assert excinfo.match(
            "Handle " + "does_not_exist" + " has not been allocated within namespace " + shm_manager.shm_namespace
        )

        # Clean up the shared memory region.
        shm_manager.sm_index.close()
        shm_manager.sm_index.unlink()

    def test_delete__expected(self):
        """
        Test that the :meth:`.ShMem.delete` functions as expected for expected inputs.
        """
        # Create a shared memory object.
        shm_manager = ShMem("test")

        # Create some data.
        a = ["Kolmogorov", "Markov", "Gauss"]

        # Write the object to shared memory.
        shm_manager.write("a", a)

        # Check if the object exists and is equal to its expected value.
        assert shm_manager.read("a") == a

        # Delete the shared memory object and handle
        shm_manager.delete("a")

        # Check that the object has been removed from shared memory, remembering that our object are namespaced.
        # This should raise a FileNotFoundError.
        with pytest.raises(FileNotFoundError) as excinfo:
            sm_object = shared_memory.SharedMemory("test_a")

        # Check that we got the correct exception string.
        assert excinfo.match("No such file or directory: '/test_a'")

        # Check that the handle has been removed from the index
        index = shm_manager.read_index()
        assert "a" not in index

        # Clean up the shared memory region.
        shm_manager.sm_index.close()
        shm_manager.sm_index.unlink()

    def test_delete__unexpected(self):
        """
        Test that the :meth:`.ShMem.delete` raises an exception in the following cases

        +--------------------------------------+----------------------------------------------------------------------+
        | description                          | reason                                                               |
        +======================================+======================================================================+
        | handle not a string                  | See if we raise :class:`TypeError` if handle is given as anything    |
        |                                      | but a string.                                                        |
        +--------------------------------------+----------------------------------------------------------------------+
        | handle not allocated                 | See if we raise :class:`ValueError` if handle does not exit.         |
        +--------------------------------------+----------------------------------------------------------------------+
        """
        # Create a shared memory object.
        shm_manager = ShMem("test")

        # Try to raise a TypeError by supplying a non-string handle.
        with pytest.raises(TypeError) as excinfo:
            shm_manager.delete(1)

        # Check that we raised the correct exception message.
        assert excinfo.match("Handle is not a valid string")

        # Try to raise a ValueError by supplying a handle that does not exist.
        with pytest.raises(ValueError) as excinfo:
            shm_manager.delete("does_not_exist")

        # See if we get the right exception.
        assert excinfo.match(
            "Handle " + "does_not_exist" + " has not been allocated within namespace " + shm_manager.shm_namespace
        )

        # Clean up the shared memory region.
        shm_manager.sm_index.close()
        shm_manager.sm_index.unlink()

    def test_update__expected(self):
        """
        Test that the :meth:`.ShMem.update` functions as expected for expected inputs.
        """
        # Create a shared memory object.
        shm_manager = ShMem("test")

        # Create some data.
        a = ["Kolmogorov", "Markov", "Gauss"]

        # Write the object to shared memory.
        shm_manager.write("a", a)

        # Check if the object exists and is equal to its expected value.
        assert shm_manager.read("a") == a

        # Create some new data and update the object in memory
        b = ["Newton", "Ada", "Kepler"]
        shm_manager.update("a", b)

        # Check if the object exists and is equal to the updated value.
        assert shm_manager.read("a") == b

        # Clean up the shared memory region.
        shm_manager.delete("a")
        shm_manager.sm_index.close()
        shm_manager.sm_index.unlink()

    def test_update__unexpected(self):
        """
        Test that the :meth:`.ShMem.update` raises an exception in the following cases

        +--------------------------------------+----------------------------------------------------------------------+
        | description                          | reason                                                               |
        +======================================+======================================================================+
        | handle not a string                  | See if we raise :class:`TypeError` if handle is given as anything    |
        |                                      | but a string.                                                        |
        +--------------------------------------+----------------------------------------------------------------------+
        | handle not allocated                 | See if we raise :class:`ValueError` if handle does not exit.         |
        +--------------------------------------+----------------------------------------------------------------------+
        """
        # Create a shared memory object.
        shm_manager = ShMem("test")

        # Try to raise a TypeError by supplying a non-string handle.
        with pytest.raises(TypeError) as excinfo:
            shm_manager.update(1, [])

        # Check that we raised the correct exception message.
        assert excinfo.match("Handle is not a valid string")

        # Try to raise a ValueError by supplying a handle that does not exist.
        with pytest.raises(ValueError) as excinfo:
            shm_manager.update("does_not_exist", [])

        # See if we get the right exception.
        assert excinfo.match(
            "Handle " + "does_not_exist" + " has not been allocated within namespace " + shm_manager.shm_namespace
        )

        # Clean up the shared memory region.
        shm_manager.sm_index.close()
        shm_manager.sm_index.unlink()

    def test_erase(self):
        """
        Tests that :meth:`.ShMem.erase` deallocates all shared memory objects handled by the :class:`.ShMem` instance.
        """
        # Create a shared memory object.
        shm_manager = ShMem("test")

        # Create some data.
        a = ["Kolmogorov", "Markov", "Gauss"]

        # Write the object to shared memory.
        shm_manager.write("a", a)

        # Check if the object exists and is equal to its expected value.
        assert shm_manager.read("a") == a

        # Erase everything from shared memory.
        shm_manager.erase()

        # Check that the object has been removed from shared memory, remembering that our object are namespaced.
        # This should raise a FileNotFoundError.
        with pytest.raises(FileNotFoundError) as excinfo:
            sm_object = shared_memory.SharedMemory("test_a")

        # Check that we got the correct exception string.
        assert excinfo.match("No such file or directory: '/test_a'")

        # Check that the index has been erased also.
        with pytest.raises(FileNotFoundError) as excinfo:
            sm_object = shared_memory.SharedMemory("test")
        assert excinfo.match("No such file or directory: '/test'")

    def test_check_self(self):
        """
        Tests that the function raises if the manager has already been erased.
        """
        # Create a shared memory object.
        shm_manager = ShMem("test")

        # Create some data.
        a = ["Kolmogorov", "Markov", "Gauss"]

        # Write the object to shared memory.
        shm_manager.write("a", a)

        # Check if the object exists and is equal to its expected value.
        assert shm_manager.read("a") == a

        # Erase everything from shared memory.
        shm_manager.erase()

        # Try to raise the exception.
        with pytest.raises(RuntimeError) as excinfo:
            shm_manager.read("a")

        # Check that reason string matches.
        assert excinfo.match("Manager has already been deallocated")
