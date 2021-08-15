"""
Main module for REST server. Launch with

.. code-block:: bash

   (sudo) uvicorn main:app --reload --host 127.0.0.1 --port 8081

"""
import json
from fastapi import FastAPI, Form, Body, File, Request
from fastapi.responses import StreamingResponse

app = FastAPI()
"""The REST server instance itself"""


@app.post("/text/anagrams")
@app.post("/text/anagrams/")
async def anagrams(json_data: Request):
    body = json.loads(bytes(await json_data.body()).decode('utf8'))
    print(body)
