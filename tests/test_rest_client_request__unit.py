"""
Unit tests for the :class:`.Request` meta object.
"""
from algosrest.client.parallel import RequestPool, ProcessPool
from algosrest.client.text import TextRest
from algosrest.client.request import Request


class TestRequest:
    """
    Test that the container API works as expected.
    """
    def test_init(self):
        """
        Does some superfiscial testing to see if we intialized correctly. Checks that our :class:`.RequestPool`,
        :class:`.ProcessPool` and :class:`.TextRest` were instantiated and that the instance variables were
        assigned correctly.
        """
        # Create our request object.
        req = Request(2, "localhost", 8081)

        # Check that everything is of the correct class.
        assert isinstance(req.req, RequestPool)
        assert isinstance(req.req.pool, ProcessPool)
        assert isinstance(req.text, TextRest)

        # Check that input data was stored correctly.
        assert req.req.hostname == "localhost"
        assert req.req.port == 8081

        # Shut down the pool.
        req.req.shutdown()
