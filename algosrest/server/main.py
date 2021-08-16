"""
Main module for REST server. Launch with

.. code-block:: bash

   (sudo) uvicorn main:app --reload --host 127.0.0.1 --port 8081

"""
import json
import subprocess
from algosrest.server.text import TextREST
from typing import Any


from fastapi import FastAPI, Form, Body, File, Request
from fastapi.responses import StreamingResponse

app = FastAPI()
"""The REST server instance itself"""


@app.get("/shutdown")
@app.get("/shutdown/")
async def shutdown():
    """
    Shuts down the server. Useful for testing when running the server in a separate thread. Works by finding the
    pid of this process and killing it.
    """
    # First grep uvicorn from the list of processes, print the second column and use that as input into kill.
    output = subprocess.check_output("kill $(ps aux | grep \"[u]vicorn.*main:app\" | awk '{print $2;}')", shell=True)


@app.post("/text/anagrams")
@app.post("/text/anagrams/")
async def anagrams(json_data: Request):
    """
    App route for :func:`algosrest.server.text.TextREST.anagrams` .

    :param Request json_data: JSON data from post request.
    :return: The JSON encoded anagrams list of lists of strings.
    """
    # Instantiate the REST helper.
    text = TextREST()

    # Get the loaded JSON response.
    body: dict[str, Any] = json.loads(bytes(await json_data.body()).decode('utf8'))

    # Call the anagrams method and get the result.
    result = text.anagrams(body)

    return result
