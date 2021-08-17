import pytest
from algosrest.client.parallel import ProcessPool


def square(x):
    """
    A simple function that squares a number. Used to test the :class:`.ProcessPool`.
    """
    return x * x


def cube(x):
    """
    A simple function that cubes a number. Used to test the :class:`.ProcessPool`.
    """
    return x * x * x


def point(x, y):
    """
    Tests handling multiple input arguments with the executor.
    """
    return x, y


class DataProcessPool:
    """
    Data for :class:`.ProcessPool`
    """
    single_batch__expected = [
        ([square, [1, 2, 3]], [1, 4, 9]),
        ([cube, [1, 2, 3]], [1, 8, 27]),
        ([point, [1, 3], [2, 4]], [(1, 2), (3, 4)])
    ]
    """
    Test data for :meth:`.ProcessPool.batch` and :meth:`.ProcessPool.single` .
    """


class TestProcessPool:
    """
    Test class for :class:`ProcessPool` 's methods.
    """
    @pytest.mark.parametrize(
        "test_input,expected",
        DataProcessPool.single_batch__expected,
        ids=[
            v[0][0].__name__ + "-" + repr(v[0][1:]) + "--" + repr(v[1]) for v in DataProcessPool.single_batch__expected
        ]
    )
    def test_batch__expected(self, test_input, expected):
        """
        Tests :meth:`.ProcessPool.batch` against expected inputs. Uses the functions and test data from
        :attr:`DataProcessPool.single_batch__expected` . This tests the function in its generalized sense, not
        with the specific types in mind.
        """
        # Give meaningful names to inputs
        func_to_map = test_input[0]
        arguments = test_input[1:]

        # Create the ProcessPool instance with three workers.
        process_pool = ProcessPool(3)

        # Get the result of the inputs applied against the function
        res = process_pool.batch(func_to_map, *arguments)

        # Coerce the iterator to list.
        res_list = list(res)

        # Clean up the pool.
        process_pool.shutdown()

        # Assert that the results are as expected
        assert res_list == expected

    @pytest.mark.parametrize(
        "test_input,expected",
        DataProcessPool.single_batch__expected,
        ids=[
            v[0][0].__name__ + "-" + repr(v[0][1:]) + "--" + repr(v[1]) for v in DataProcessPool.single_batch__expected
        ]
    )
    def test_single__expected(self, test_input, expected):
        """
        Tests :meth:`.ProcessPool.single` against expected inputs. Uses the functions and test data from
        :attr:`DataProcessPool.single_batch__expected` . This tests the function in its generalized sense, not
        with the specific types in mind.
        """
        # Give meaningful names to inputs
        func_to_map = test_input[0]
        arguments = test_input[1:]

        # Create the ProcessPool instance with three workers.
        process_pool = ProcessPool(3)

        # Create a list to store the single results
        res_list = list()

        # Transpose items so that they can be given as args.
        sorted_arguments = list(map(list, zip(*arguments)))

        # Make the requests for each argument in the sorted list.
        for arg in sorted_arguments:
            # Get the result of the inputs applied against the function
            res = process_pool.single(func_to_map, *arg)
            res_list.append(res.result())

        # Clean up the pool.
        process_pool.shutdown()

        assert res_list == expected

    def test_shutdown(self):
        """
        Tests :meth:`.ProcessPool.shutdown`. We make a request, call the shutdown and make another request. The
        second request should raise an exception.
        """
        # Create an instance of the process pool.
        process_pool = ProcessPool(3)

        # Make a request to see if it is working.
        res = process_pool.single(square, 2)

        # Check if we got the correct response.
        assert res.result() == 4

        # Shutdown the pool.
        process_pool.shutdown()

        # Make a request to see if it is still working.
        with pytest.raises(RuntimeError) as excinfo:
            res = process_pool.single(square, 2)
            assert excinfo.value == "cannot schedule new futures after shutdown"
