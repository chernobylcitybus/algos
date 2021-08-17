Algos
=====

[![Build Status](https://travis-ci.com/8563a236e65cede7b14220e65c70ad5718144a3/algos.svg?branch=master)](https://travis-ci.com/8563a236e65cede7b14220e65c70ad5718144a3/algos)
[![Coverage Status](https://coveralls.io/repos/github/8563a236e65cede7b14220e65c70ad5718144a3/algos/badge.svg)](https://coveralls.io/github/8563a236e65cede7b14220e65c70ad5718144a3/algos)

Introduction
------------

This repository aims to be the fully type annotated version of the algorithms presented in 
*Competitive Programming in Python by Durr and Vie*. Algorithms are grouped logically for the purpose of packaging.
For a chapter by chapter version, see 
https://github.com/8563a236e65cede7b14220e65c70ad5718144a3/Competitive_Programming_in_Python .

This library aims to have full type annotations, not just for function signatures but also local variables to ensure
that compilation to C with `mypyc` is possible for all the algorithms. The code presented herein relies only upon the
Python3 standard library, which is already fully type annotated. As a result, a complete static analysis has been 
performed on the code, both with `mypy` and when `mypyc` passes the code to `gcc`.

Documentation
-------------

To build the documentation you will need to have a working LaTeX installation. On Debian, this can be
achieved with

    sudo apt install texlive-full
    sudo apt install texlive-latex-extra

You will also need Sphinx and the Read the Docs Theme. These dependencies are automatically taken care of when you 
install the package.

    python3.9 -m pip install sphinx sphinx_rtd_theme

You can then create the documentation as follows

    bash scripts/make_docs.sh

Please use the script in order to be able to generate documentation for the tests folder. It adds an \_\_init\_\_.py
so that sphinx picks up the folder.

Installation
------------

To install the package one simply issues

    python3.9 -m pip install .

If you would like to install the package in editable mode, you can use

    python3.9 -m pip install --editable .

In editable mode, you can pull the latest code, and the package will automatically be up to date on your system. 
However, if command line features have been added (console scripts in setup.py), to access them you will need to issue
the commands

    python3.9 -m pip uninstall algos
    python3.9 -m pip install --editable .

This will create the new entry points that your shell can use.

Testing
-------

There are over 100 tests so far. Both unit tests and integration tests are carried out simultaneously with
no special setup needed.

To run the test suite, simply issue

    $ pytest -sv tests/

To run a specific test, issue

    $ pytest -sv tests/test_to_run.py

To run the full coverage suite, we can use

    $ pytest -sv --cov=algos --cov=algoscli --cov=algosrest --cov-report=html tests/

Static Analysis and Optimization
--------------------------------

``mypy`` has been used throughout the project. In the vast majority of cases, all variables have been statically
typed, whether interfaces, local variables or class variables.

To perform static analysis for the entire project, one can issue

.. code-block:: bash

   $ mypy algos algoscli algosrest
   Success: no issues found in 13 source files

To perform static analysis for a signle file, we can use

    $ mypy algos/io.py
    Success: no issues found in 1 source file

Due to strictly typing most of the variables, we can gain a quick optimization by using `mypyc` to compile our
code down to Python C extensions. The speed up may range anywhere by up to 4 times, or over while sticking to
standard Python syntax.

Observe the following sequence of steps

    $ tree algos algoscli algosrest -I __pycache__
    algos
    ├── __init__.py
    ├── io.py
    └── text.py
    algoscli
    ├── common.py
    ├── __init__.py
    ├── main.py
    └── text.py
    algosrest
    ├── client
    │   ├── __init__.py
    │   └── parallel.py
    ├── __init__.py
    └── server
        ├── __init__.py
        ├── main.py
        └── text.py
    
    $ mypyc algos algoscli algosrest/client
    running build_ext
    building '013d4d1ac8d707eadf97__mypyc' extension
    gcc -pthread -Wno-unused-result -Wsign-compare ...
    
    $ tree algos algoscli algosrest -I __pycache__
    algos
    ├── __init__.cpython-39-x86_64-linux-gnu.so
    ├── __init__.py
    ├── io.cpython-39-x86_64-linux-gnu.so
    ├── io.py
    ├── text.cpython-39-x86_64-linux-gnu.so
    └── text.py
    algoscli
    ├── common.cpython-39-x86_64-linux-gnu.so
    ├── common.py
    ├── __init__.cpython-39-x86_64-linux-gnu.so
    ├── __init__.py
    ├── main.cpython-39-x86_64-linux-gnu.so
    ├── main.py
    ├── text.cpython-39-x86_64-linux-gnu.so
    └── text.py
    algosrest
    ├── client
    │   ├── __init__.cpython-39-x86_64-linux-gnu.so
    │   ├── __init__.py
    │   ├── parallel.cpython-39-x86_64-linux-gnu.so
    │   └── parallel.py
    ├── __init__.py
    └── server
        ├── __init__.py
        ├── main.py
        └── text.py

We can now see the compiled libraries present in the packages, alongside their source files.

Command Line Usage
------------------

A small example to get started would be

    $ echo "below on the elbow is the bowel" | algos-text anagrams | cut -b1-10
    [['below',

The command line interface is made up of command line groupings e.g. ``algos-text``. Within each command line grouping,
there can be a variety of functions. In our case, we are calling the sub-command ``anagrams`` within the ``algos-text``
utility group. The `cli` accepts string input in ``stdin`` and prints to ``stdout`` . The output can be piped
to other utilities and chained indefinitely. A future improvement will be an eval function, that allows python string
representations of data types to be eval'd and used as inputs to the command line algorithms. This would alleviate the
need to convert to and from a plain text representation for each link of the chain.

REST API Server Usage
---------------------

We start the server with the standard ``uvicorn`` usage.

    $ uvicorn main:app --reload --host 127.0.0.1 --port 8081

If you want to listen for connections outside the localhost, use

    $ uvicorn main:app --reload --host 0.0.0.0 --port 8081

We can use curl to verify that the server is operational

    $ curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"input": "below on the elbow is the bowel"}' \
    http://localhost:8081/text/anagrams
    
    [["bowel","below","elbow"]]

REST API Client Usage
---------------------

One should start the rest server first. Then, one can perform single requests or batch requests with the multiprocessing
backend.

A single request looks like

    # We are targeting the root endpoint of the REST API.
    root_req = RequestInfo(endpoint="/", method="GET")

    # Create a RequestPool with two workers.
    req = RequestPool(1, "localhost", 8081)

    # Perform a request to the root endpoint.
    res = req.single_request(root_req)

    # Clean up the process pool.
    req.shutdown()

    # Await the result.
    res_data = res.result()
