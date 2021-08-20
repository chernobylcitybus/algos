"""
`Conftest <https://docs.pytest.org/en/6.1.2/writing_plugins.html#localplugin>`_
allows the creation of local plugins for pytest. This module should never be imported as pytest reads it in for the
tests.

Contains a variety of fixtures that will have scope for all tests.
"""
import pytest
import threading
import time
import os
import subprocess


class MockHTTPResponse:
    """
    This class mocks the class :class:`http.client.HTTPResponse` that is the result of a request made by class
    :class:`http.client.HTTPConnection` . It had just one method, read, that returns the :class:`bytes` buffer
    that it was given upon initialization.

    :ivar bytes buffer: A binary buffer that contains the expected server response.

    .. automethod:: __init__

    """
    def __init__(self, buffer: bytes):
        """
        Initializes the object with the data to return.

        :param buffer: The mock data to return.
        """
        self.buffer = buffer

    def read(self):
        """
        Simulates the :meth:`http.client.HTTPResponse.read` method so that we can successfully mock responses in our
        :mod:`algosrest.client` unit tests.

        :return: The data the object was initialized with.
        """
        return self.buffer


class MockHTTPConnection:
    """
    This mocks the class :class:`http.client.HTTPConnection` that :mod:`http.client` uses to perform HTTP requests.
    This is primary used by :meth:`algosrest.client.parallel.RequestPool.request` to perform the REST requests. This
    is the point of egress out of our code and into the standard library, as far as our client is concerned.

    This simulates four of the actual :class:`http.client.HTTPConnection` methods. Namely, __init__, request,
    getresponse and close as these are the methods used by :meth:`algosrest.client.parallel.RequestPool.request` .

    The buffer is used by the tests to store the expected server responses. It can be a simple bytes object or a
    list of bytes objects. It can also be a dictionary in a multiprocessing situation, when the request body is used
    as the key that produces the server's expected response as a value. This stops race conditions when more than
    one worker process is used.

    :ivar str hostname: The hostname of the remote server. Just stores this because it is parsed in through the
                        function signature.
    :ivar str hostname: The port of the remote server. Just stores this because it is parsed in through the
                        function signature.
    :ivar bytes current_request: The json body of the request that was made to the connection. Used when in a
                                 multiprocessing situation so that multiple processes get the correct out of order
                                 responses, as reading from a buffer linearly is a race condition.

    .. automethod:: __init__

    """
    buffer = b"Hello"
    """
    A buffer to hold the expected responses. Can be a :class:`bytes` object, a list of :class:`bytes` objects or
    a dictionary that produces :class:`bytes` values, depending on the test scenario. When more than one worker is 
    involved, it is necessary to use the dictionary approach to prevent race conditions. The list approach is fine when 
    testing one worker process that consumes multiple inputs. If you need to test a single worker which only consumes 
    one input, the :class:`bytes` object approach works easiest.
    """

    def __init__(self, hostname, port):
        """
        Initializes the mock. The initial information is not used by the mock.

        :param str hostname: The hostname of the remote server.
        :param str port: The port of the REST server.
        """
        self.hostname = hostname
        self.port = port
        self.current_request = ""

    def request(self, *args, **kwargs):
        """
        The :class:`MockHTTPConnection` is a different instance for each multiprocessing worker i.e. a different
        object in memory for each. So, assigning the request body to the :attr:`MockHTTPConnect.current_request`
        variable works safely, as it is sequentially servicing one process.
        """
        # Get the body
        body = kwargs.get("body")

        self.current_request = kwargs.get("body")
        pass

    def getresponse(self):
        """
        Return the expected response for the tests. Handles the cases that the buffer is a bytes object, list or
        dictionary, depending on which the current test chooses to use.

        :return: Server expected response.
        """
        if isinstance(self.buffer, bytes):
            # Return the buffer itself.
            mock_res = MockHTTPResponse(self.buffer)
        elif isinstance(self.buffer, list):
            # Pop the first element off the buffer.
            mock_res = MockHTTPResponse(self.buffer.pop(0))
        elif isinstance(self.buffer, dict):
            # Use the body of the request as the key to find the value of the expected response.
            mock_res = MockHTTPResponse(self.buffer[self.current_request])
        return mock_res

    def close(self):
        """
        A method that does nothing but is required for the purposes of the mock.
        """
        pass


def start_server():
    """
    Start the server process in a separate thread. This opens a subprocess with the command ``uvicorn mainLapp --reload
    --host 127.0.0.1 --port 8081`` .
    """
    os.chdir("algosrest/server/")
    subprocess.Popen(["uvicorn", "main:app", "--reload", "--host", "127.0.0.1", "--port", "8081"],
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    os.chdir("../..")


@pytest.fixture(scope="class")
def rest_server_fixture():
    """
    A fixture that actually runs the current development version of the server. It is used by both the rest client
    integration tests and the rest server integration tests. The fixture has class scope. You need only include
    it in your test function signature to have it available. As it has class scope, your test will need to be
    grouped into an appropriate class to be able to use the fixture i.e.

    .. code-block:: py

       class TestX:
           def test_xxx(rest_server_fixture, ...):
               make_rest_request()

    """
    # Start the server in a thread.
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    # Sleep a bit.
    time.sleep(1)

    # Yield something to keep it going.
    yield 1

    # Shutdown the server.
    subprocess.check_output("curl -s http://localhost:8081/shutdown", shell=True)

    # Wait a bit.
    time.sleep(1)

