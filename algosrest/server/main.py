"""
Main module for REST server. Launch with

.. code-block:: bash

   (sudo) uvicorn backtester:app --reload --host 127.0.0.1 --port 8081

"""
from fastapi import FastAPI, Form, Body, File, Request
from fastapi.responses import StreamingResponse

