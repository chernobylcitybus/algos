"""
Tests the endpoints in main that aren't called from other modules.
"""
import json
import pytest
import subprocess
from algosrest.server.main import app

from fastapi.testclient import TestClient
from fastapi import Response

client: TestClient = TestClient(app)


def test_shutdown():
    """
    Check if the shutdown shell command is called. This will effectively error out with a
    :class:`subprocess.CalledProcessError` as the `.TestClient` does not actually create a server instance that
    is visible as a process. However, by the fact that the command is called and errors, we know in production that
    the signal will be sent to our REST server.
    """
    with pytest.raises(subprocess.CalledProcessError):
        client.get("/shutdown")


def test_root():
    """
    Check if the root endpoint returns a status message.
    """
    resp = client.get("/")

    assert resp.status_code == 200
    assert resp.json() == {"status": "okay"}


def test_post_root():
    """
    Check if posting to the root endpoint yields the data sent with the POST request.
    """
    response: Response = client.post("/", json={"hello": "world"})

    assert response.status_code == 200
    assert response.json() == {"hello": "world"}