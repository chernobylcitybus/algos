import pytest
from algosrest.client.parallel import RequestPool


class TestRequestPool:
    def notest_single_request__expected(self, rest_server):
        req = RequestPool(1)

