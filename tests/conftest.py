"""
`Conftest <https://docs.pytest.org/en/6.1.2/writing_plugins.html#localplugin>`_
allows the creation of local plugins for pytest. This module should never be imported as pytest reads it in for the
tests.

Contains a variety of fixtures that will have scope for all tests.
"""
import io
import http.client
import pytest
import threading
import time
import os
import subprocess
import json


class MockHTTPResponse:
    def __init__(self, buffer: bytes):
        self.buffer = buffer

    def read(self):
        return self.buffer


class MockHTTPConnection:

    buffer = b"Hello"

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.current_request = ""

    def request(self, *args, **kwargs):
        """
        The :class:`MockHTTPConnection` is a different instance for each multiprocessing worker i.e. a different
        object in memory for each. So, assigning the request body to the :attr:`MockHTTPConnect.current_request`
        variable works safely, as it is linearly servicing one process.
        """
        # Get the body
        body = kwargs.get("body")

        self.current_request = kwargs.get("body")
        pass

    def getresponse(self):
        if isinstance(self.buffer, bytes):
            mock_res = MockHTTPResponse(self.buffer)
        elif isinstance(self.buffer, list):
            mock_res = MockHTTPResponse(self.buffer.pop(0))
        elif isinstance(self.buffer, dict):
            mock_res = MockHTTPResponse(self.buffer[self.current_request])
        return mock_res

    def close(self):
        pass


def start_server():
    """
    Start the server process in a separate thread.
    """
    os.chdir("algosrest/server/")
    subprocess.Popen(["uvicorn", "main:app", "--reload", "--host", "127.0.0.1", "--port", "8081"],
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    os.chdir("../..")


@pytest.fixture(scope="class")
def rest_server_fixture():
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

