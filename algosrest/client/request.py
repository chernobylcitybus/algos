"""
A general container for all the modules REST implementations. Can be used for convenience and to reuse a single
:class:`.RequestPool` for all algorithms.
"""
from algosrest.client.parallel import RequestPool
from algosrest.client.text import TextRest


class Request:
    """
    Houses the different REST implementations.

    :ivar RequestPool req: The pool of workers with which to perform the requests.
    :ivar TextRest text: Interface for text based algorithms.
    """
    def __init__(self, n_workers: int, hostname: str, port: int):
        """
        Initializes a pool of n_workers to make concurrent requests. Also assigns REST interfaces to convenient
        names.

        :param int n_workers: The number of workers you would like in the :class:`.RequestPool` .
        :param str hostname: A valid hostname to connect to.
        :param int port: The port that the REST server is listening on.
        """
        self.req = RequestPool(n_workers, hostname, port)
        self.text = TextRest(self.req)
