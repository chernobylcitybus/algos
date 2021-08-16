import pytest
from algosrest.client.parallel import ProcessPool


def square(x):
    """
    A simple function that squares a number. Used to test the :class:`ProcessPool`.
    """
    return x * x


def cube(x):
    """
    A simple function that cubes a number. Used to test the :class:`ProcessPool`.
    """
    return x * x * x


class DataProcessPool:
    batch__expected = [
        ([square, [1, 2, 3]], [1, 4, 9]),
        ([cube, [1, 2, 3]], [1, 8, 27]),
    ]
    """
    Test data for :meth:`ProcessPool.batch` and :meth:`ProcessPool.single` .
    """


class TestProcessPool:
    """
    Test class for :class:`ProcessPool` 's methods.
    """
    @pytest.mark.parametrize(
        "test_input,expected",
        DataProcessPool.batch__expected,
        ids=[v[0][0].__name__ + "-" + repr(v[0][1]) + "--" + repr(v[1]) for v in DataProcessPool.batch__expected]
    )
    def test_batch__expected(self, test_input, expected):
        """
        Tests :meth:`ProcessPool.batch` against expected inputs. Uses the functions and test data from
        :attr:`DataProcessPool.batch__expected` .
        """
        # Give meaningful names to inputs
        func_to_map = test_input[0]
        arguments = test_input[1]

        # Create the ProcessPool instance with three workers.
        process_pool = ProcessPool(3)

        # Get the result of the inputs applied against the function
        res = process_pool.batch(func_to_map, arguments)

        # Coerce the iterator to list.
        res_list = list(res)

        # Clean up the pool.
        process_pool.shutdown()

        # Assert that the results are as expected
        assert res_list == expected
