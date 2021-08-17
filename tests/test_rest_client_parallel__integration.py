import pytest
import json
from algosrest.client.parallel import RequestPool, RequestInfo


class TestRequestPool:
    """
    Test class for :class:`.RequestPool` .
    """
    def test_batch_request__expected(self, rest_server):
        req = RequestPool(1, "localhost", 8081)
        req_infos = [[RequestInfo(endpoint="/", method="GET")]]

        res = list(req.batch_request(req_infos))

        assert json.loads(res[0][0][0]) == {"status": "okay"}
        assert res[0][0][2] == "/"

