"""
Unit Tests for :mod:`algosrest.client.parallel` .
"""
import pytest
from algosrest.client.parallel import ProcessPool, RequestPool, RequestInfo


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


class DataRequestInfo:
    init__expected = [
        (["a", "GET", None], RequestInfo(endpoint="a", method="GET")),
        (["b", "POST", {"data": "something"}], RequestInfo(endpoint="b", method="POST", data={"data": "something"}))
    ]
    """
    Test data for :meth:`.RequestInfo.__init__` that contains expected inputs for this function. Also used by
    the test :meth:`TestRequestInfo.test_eq__expected`
    """

    init__unexpected = [
        ([list(), "GET", None], [TypeError, "Invalid type for endpoint - <class 'list'>"]),
        ([set(), "GET", None], [TypeError, "Invalid type for endpoint - <class 'set'>"]),
        (["/", list(), None], [TypeError, "Invalid type for method - <class 'list'>"]),
        (["/", set(), None], [TypeError, "Invalid type for method - <class 'set'>"]),
        (["/", "HELP", None], [ValueError, "Invalid value for method. Must be 'GET' or 'POST'"]),
        (["/", "POST", "string"], [TypeError, "Invalid type for data - <class 'str'>"]),
        (["/", "POST", None], [ValueError, "No data given for POST request"]),
        (["/", "GET", {}], [ValueError, "Data supplied for GET request"])
    ]
    """
    Test data for :meth:`.RequestInfo.__init__` that contains bad input values, and the expected exceptions they
    should raise.
    """


class DataProcessPool:
    """
    Data for :class:`.ProcessPool` .
    """
    single_batch__expected = [
        ([square, [1, 2, 3]], [1, 4, 9]),
        ([cube, [1, 2, 3]], [1, 8, 27]),
        ([point, [1, 3], [2, 4]], [(1, 2), (3, 4)])
    ]
    """
    Test data for :meth:`.ProcessPool.batch` and :meth:`.ProcessPool.single` .
    """


class DataRequestPool:
    """
    Data for :class:`.RequestPool` .
    """
    chunks__expected = [
        (
            [1, [RequestInfo(endpoint=x, method="GET") for x in ["a", "b", "c"]]],
            [[RequestInfo(endpoint=x, method="GET")] for x in ["a", "b", "c"]]
        ),
        (
            [2, [RequestInfo(endpoint=x, method="GET") for x in ["a", "b", "c"]]],
            [[RequestInfo(endpoint=x, method="GET") for x in ["a", "b"]]] +
            [[RequestInfo(endpoint=x, method="GET") for x in ["c"]]]
        )
    ]
    """
    Test data for :meth:`.RequestPool.chunks`.
    """

    chunks__unexpected = [
        ([list(), None], [TypeError, "Invalid input type for n - <class 'list'>"]),
        ([2, dict()], [TypeError, "Invalid input type for array - <class 'dict'>"]),
        (
            [2, [1, RequestInfo(endpoint="a", method="GET")]],
            [TypeError, "Invalid input type for array element"]
         )
    ]
    """
    Test data for :meth:`.RequestPool.chunks` and exceptions raised.
    """

    init__unexpected = [
        ([[1], "localhost", 8081], [TypeError, "Number of workers not given as int"]),
        ([1, 1, 8081], [TypeError, "Hostname not given as string"]),
        ([1, "localhost", "8081"], [TypeError, "Port not given as int"]),
        ([1, "", 8081], [ValueError, "Blank hostname given"]),
        ([1, "localhost", 0], [ValueError, "Invalid port number given"]),
    ]
    """
    Test data for :meth:`.RequestPool.__init__` and exceptions raised.
    """


class TestRequestInfo:
    """
    Test class for :class:`.RequestInfo` 's construction and dunder methods.
    """
    @pytest.mark.parametrize(
        "test_input,expected",
        DataRequestInfo.init__expected,
        ids=[
            repr(v) for v in DataRequestInfo.init__expected
        ]
    )
    def test_eq__expected(self, test_input, expected):
        """
        Tests that :meth:`.RequestInfo.__eq__` returns the expected value when constructed from the expected inputs.
        Uses data :attr:`DataRequestInfo.init__expected` .
        """
        # Assign the test input to meaningful names.
        endpoint = test_input[0]
        method = test_input[1]
        data = test_input[2]

        # Instantiate the RequestInfo object with the inputs.
        req = RequestInfo(endpoint=endpoint, method=method, data=data)

        assert req.endpoint == expected.endpoint
        assert req.method == expected.method
        assert req.data == req.data

    def test_eq__unexpected(self):
        """
        Tests that :meth:`.RequestInfo.__eq__` tests False if being compared to another object and is False if
        the attributes of two :class:`RequestInfo` instances are not the same.
        """
        # Check that we return fast when the other object is not a RequestInfo.
        req1 = RequestInfo(endpoint="/", method="GET")
        assert not (req1 == list())

        # Check that they differ when endpoints differ.
        req2 = RequestInfo(endpoint="/hello", method="GET")
        assert not (req2 == req1)

        # Check that they differ when methods differ.
        req3 = RequestInfo(endpoint="/hello", method="POST", data={})
        assert not (req3 == req2)

        # Check that they differ if data differs.
        req4 = RequestInfo(endpoint="/hello", method="POST", data={"a": "string"})
        assert not (req4 == req3)

    @pytest.mark.parametrize(
        "test_input,expected",
        DataRequestInfo.init__expected,
        ids=[
            repr(v) for v in DataRequestInfo.init__expected
        ]
    )
    def test_init__expected(self, test_input, expected):
        """
        Test that :meth:`.RequestInfo.__init__` initializes the class correctly for expected inputs. We create the
        object from the test inputs and check using :meth:`.RequestInfo.__eq__` that the instantiated class is the
        same as the expected value. Uses data :attr:`DataRequestInfo.init__expected` .
        """
        # Assign the test input to meaningful names.
        endpoint = test_input[0]
        method = test_input[1]
        data = test_input[2]

        # Instantiate the RequestInfo object with the inputs.
        req = RequestInfo(endpoint=endpoint, method=method, data=data)

        # Check for equality.
        assert req == expected

    @pytest.mark.parametrize(
        "test_input,error",
        DataRequestInfo.init__unexpected,
        ids=[
            repr(v) for v in DataRequestInfo.init__unexpected
        ]
    )
    def test_init__unexpected(self, test_input, error):
        """
        Test that :meth:`.RequestInfo.__init__` raises on invalid input values. We attempt to create an instance
        and see if the raised error matches what we expected.
        """
        # Assign the test input to meaningful names.
        endpoint = test_input[0]
        method = test_input[1]
        data = test_input[2]

        # Try to raise the exception

        with pytest.raises(error[0]) as excinfo:
            # Instantiate the RequestInfo object with the inputs.
            req = RequestInfo(endpoint=endpoint, method=method, data=data)

        # Check if the error string is correct.
        assert excinfo.match(error[1])

    def test_repr(self):
        """
        Test that the text representation of :class:`.RequestInfo` is correct.
        """
        req = RequestInfo(endpoint="/", method="GET")
        assert repr(req) == "RequestInfo(/, GET, None)"

        req = RequestInfo(endpoint="/", method="POST", data={"a": "b"})
        assert repr(req) == "RequestInfo(/, POST, {'a': 'b'})"


class TestProcessPool:
    """
    Test class for :class:`.ProcessPool` 's methods.
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

        # Check that the error string is correct.
        assert excinfo.match("cannot schedule new futures after shutdown")


class TestRequestPool:
    """
    Test class for :class:`.RequestPool` .
    """
    @pytest.mark.parametrize(
        "test_input,error",
        DataRequestPool.init__unexpected,
        ids=[repr(v) for v in DataRequestPool.init__unexpected]
    )
    def test_init__unexpected(self, test_input, error):
        """
        Test that :meth:`RequestPool.chunks` raises exceptions on invalid input in
        :attr:`DataRequestPool.init__unexpected` .
        """
        # Assign input to meaningful names.
        n_workers = test_input[0]
        hostname = test_input[1]
        port = test_input[2]

        # Try to raise the exceptions.
        with pytest.raises(error[0]) as excinfo:
            req = RequestPool(n_workers, hostname, port)

        # Check that the error string is correct.
        assert excinfo.match(error[1])
        
    @pytest.mark.parametrize(
        "test_input,expected",
        DataRequestPool.chunks__expected,
        ids=[v for v in range(len(DataRequestPool.chunks__expected))]
    )
    def test_chunks__expected(self, test_input, expected):
        """
        Test :meth:`RequestPool.chunks` using expected inputs :attr:`DataRequestPool.chunks__expected` .
        """
        # Assign input to meaningful names.
        chunks = test_input[0]
        test_data = test_input[1]
        
        # Create the RequestPool.
        req = RequestPool(1, "localhost", 8081)
        
        # Split the input into chunks.
        res = list(req.chunks(test_data, chunks))
        
        # Shutdown the RequestPool.
        req.shutdown()

        # Check that the results are as expected.
        assert res == expected

    @pytest.mark.parametrize(
        "test_input,error",
        DataRequestPool.chunks__unexpected,
        ids=[repr(v) for v in DataRequestPool.chunks__unexpected]
    )
    def test_chunks__unexpected(self, test_input, error):
        """
        Test that :meth:`RequestPool.chunks` raises exceptions on invalid input in
        :attr:`DataRequestPool.chunks__unexpected` .
        """
        # Assign input to meaningful names.
        chunks = test_input[0]
        test_data = test_input[1]

        # Create the RequestPool.
        req = RequestPool(1, "localhost", 8081)

        # Try to raise the exceptions.
        with pytest.raises(error[0]) as excinfo:
            res = list(req.chunks(test_data, chunks))

        # Shutdown the RequestPool.
        req.shutdown()

        # Check that the error string is correct.
        assert excinfo.match(error[1])

    def test_shutdown(self):
        """
        Tests :meth:`.RequestPool.shutdown`. We make a request, call the shutdown and make another request. The
        second request should raise an exception.
        """
        # Create an instance of the process pool.
        request_pool = RequestPool(1, "localhost", 8085)

        # Make a request to see if it is working.
        res = request_pool.pool.single(square, 2)

        # Check if we got the correct response.
        assert res.result() == 4

        # Shutdown the pool.
        request_pool.shutdown()

        # Make a request to see if it is still working.
        with pytest.raises(RuntimeError) as excinfo:
            res = request_pool.pool.single(square, 2)

        # Check that the error string is correct.
        assert excinfo.match("cannot schedule new futures after shutdown")

    def test_batch_request__expected(self):
        req = RequestPool(1, "localhost", 8081)
        req_infos = [[RequestInfo(endpoint="/", method="GET")]]

        res = list(req.batch_request(req_infos))
        print(res)