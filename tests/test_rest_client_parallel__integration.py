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
    Test data for :meth:`.RequestInfo.batch_request` to verify that the correct responses are returned.
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
        req = RequestPool(2, "localhost", 8081)
        req_infos = test_input

        res = list(req.batch_request(req_infos))
        res_cleaned = [[[json.loads(y[0]), y[2]] for y in x] for x in res]

        assert res_cleaned == expected

