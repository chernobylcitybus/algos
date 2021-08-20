"""
Tests the endpoints in main that aren't called from other modules.
"""
import json
import textwrap
import time
import threading
import subprocess
from .conftest import start_server


def test_shutdown():
    """
    Check if the shutdown shell command is called.
    """
    # Start the server in a thread.
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    # Sleep a bit
    time.sleep(1)

    # Check if the thread has started.
    pid: bytes = subprocess.check_output("echo $(ps aux | grep \"[u]vicorn.*main:app\" | awk '{print $2;}')", shell=True)

    # Call shutdown.
    subprocess.check_output("curl -s http://localhost:8081/shutdown", shell=True)

    # Sleep a bit
    time.sleep(1)

    # Check if the thread terminated.
    terminated: bytes = subprocess.check_output("echo $(ps aux | grep \"[u]vicorn.*main:app\")", shell=True)

    # Get string versions of process output.
    pid_str = pid.decode().strip()
    terminated_str = terminated.decode().strip()

    # Join the thread.
    server_thread.join()

    # Assert that the pid was a number and terminated was an empty string.
    assert isinstance(int(pid_str), int)
    assert terminated_str == ""


class TestMain:
    """
    We make use of a class to test the functions in an integration test setting as we need access to the
    :func:`.rest_server_fixture` in order to run an actual instance of the development server.
    """
    def test_root(self, rest_server_fixture):
        """
        Check if the root endpoint returns a status message.
        """
        # Make a request to the root endpoint with curl.
        output = subprocess.check_output("curl -s http://localhost:8081/", shell=True)

        # Check that the result is as expected.
        assert json.loads(output.decode()) == {"status": "okay"}

    def test_post_root(self, rest_server_fixture):
        """
        Check if the root endpoint returns the data sent with the POST request.
        """
        # Make a request to the root endpoint with curl.
        post_request = textwrap.dedent(
            f"""
            curl -s --header "Content-Type: application/json"   --request POST   
            --data '{json.dumps({"hello": "world"})}'   http://localhost:8081/
            """
        ).replace("\n", " ")
        post_output: bytes = subprocess.check_output(post_request, shell=True)

        # Check that the result is as expected.
        assert json.loads(post_output.decode()) == {"hello": "world"}
