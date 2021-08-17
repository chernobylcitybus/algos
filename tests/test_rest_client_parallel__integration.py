import pytest
import json
from algosrest.client.parallel import RequestPool, RequestInfo


root_req = RequestInfo(endpoint="/", method="GET")
"""
:class:`RequestInfo` for request to root server endpoint.
"""

root_req_res = [{"status": "okay"}, "/"]
"""
Response from the rest server when performing a request to the root endpoint.
"""


class DataRequestPool:
    """
    Contains data for :class:`.RequestPool` tests.
    """
    batch__expected = [
        ([[root_req]], [[root_req_res]]),
        ([[root_req, root_req]], [[root_req_res, root_req_res]]),
        ([[root_req], [root_req]], [[root_req_res], [root_req_res]]),


    ]
    """
    Test data for :meth:`.RequestPool.batch_request` to verify that the correct responses are returned.
    """


class TestRequestPool:
    """
    Test class for :class:`.RequestPool` .
    """
    @pytest.mark.parametrize(
        "test_input,expected",
        DataRequestPool.batch__expected,
        ids=[str(v) for v in range(len(DataRequestPool.batch__expected))]
    )
    def test_batch_request__expected(self, rest_server, test_input, expected):
        """
        Tests :meth:`.RequestPool.batch_request` . The input data used is :attr:`DataRequestPool.batch__expected` ,
        with corresponding expected output. The latest version of the :func:`.rest_server` is used to receive
        the requests and send back the responses.
        """
        # Create a RequestPool with two workers.
        req = RequestPool(2, "localhost", 8081)

        # Set the RequestInfo array to the test input.
        req_infos = test_input

        # Make the request.
        res = list(req.batch_request(req_infos))

        # Exclude timings from results.
        res_cleaned = [[[json.loads(y[0]), y[2]] for y in x] for x in res]

        # Clean up the process pool.
        req.shutdown()

        # Verify that the results are as expected.
        assert res_cleaned == expected

    def test_single_request__expected(self, rest_server):
        """
        Tests :meth:`.RequestPool.single_request` . The latest version of the :func:`.rest_server` is used to receive
        the requests and send back the responses.
        """
        # Create a RequestPool with two workers.
        req = RequestPool(1, "localhost", 8081)

        # Perform a request to the root endpoint.
        res = req.single_request(root_req)

        # Clean up the process pool.
        req.shutdown()

        # Await the result.
        res_data = res.result()

        # Map the response to meaningful names.
        status = json.loads(res_data[0][0])
        endpoint = res_data[0][2]

        # Check that they were as expected.
        assert [status, endpoint] == root_req_res

