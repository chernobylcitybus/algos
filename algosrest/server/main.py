"""
Main module for REST server. Launch with

.. code-block:: bash

   (sudo) uvicorn main:app --reload --host 127.0.0.1 --port 8081

"""
import json
from algosrest.server.text import TextREST
from typing import Any


from fastapi import FastAPI, Form, Body, File, Request
from fastapi.responses import StreamingResponse

app = FastAPI()
"""The REST server instance itself"""


@app.post("/text/anagrams")
@app.post("/text/anagrams/")
async def anagrams(json_data: Request):
    """
    Handler for :func:`algos.text.anagrams` .

    :param Request json_data: JSON data from post request.
    :return:
    """
    # Instantiate the REST helper.
    text = TextREST()

    # Get the loaded JSON response.
    body: dict[str, Any] = json.loads(bytes(await json_data.body()).decode('utf8'))

    # Call the anagrams method and get the result.
    result = text.anagrams(body)

    return result
