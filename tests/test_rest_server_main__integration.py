"""
Tests the endpoints in main that aren't called from other modules.
"""
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
