"""
Tests the endpoints in main that aren't called from other modules.
"""
import pytest
import os
import time
import threading
import subprocess


def start_server():
    """
    Start the server process in a separate thread.
    """
    os.chdir("algosrest/server/")
    subprocess.Popen(["uvicorn", "main:app", "--reload", "--host", "127.0.0.1", "--port", "8081"],
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    os.chdir("../..")


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
    subprocess.check_output("curl http://localhost:8081/shutdown", shell=True)

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
