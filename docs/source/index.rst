.. Algos documentation master file, created by
   sphinx-quickstart on Fri Aug 13 19:02:51 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Algos's documentation!
=================================

**Introduction**

This package aims to support general algorithm usage through three APIs. The first api :any:`algos` is a pure
Python interface and is where the actual algorithmic work is done. The next api :any:`cli` represents a
command line interface to the :any:`algos` package. The last API is a REST API, :any:`rest`. This is divided
into two further APIs, :any:`rest_client` and :any:`rest_server` . The server is a fully fledged REST
API built atop `fastapi`. The client is a REST client that performs the requests. The client is fully
multiprocessing enabled to support server-side parallel computation. The :any:`tests` package has all the unit and
integration tests, for all components. The test case data is also included, and appropriately cross referenced with
the functions being tested.

**Installation**

To install the package one simply issues

.. code-block:: bash

   python3.9 -m pip install .

If you would like to install the package in editable mode, you can use

.. code-block:: bash

   python3.9 -m pip install --editable .

In editable mode, you can pull the latest code, and the package will automatically be up to date on your system.
However, if command line features have been added (console scripts in setup.py), to access them you will need to issue
the commands

.. code-block:: bash

   python3.9 -m pip uninstall algos
   python3.9 -m pip install --editable .

This will create the new entry points that your shell can use.

**Documentation**

To build the documentation you will need to have a working LaTeX installation. On Debian, this can be
achieved with

.. code-block:: bash

   $ apt install texlive-full
   $ apt install texlive-latex-extra

You will also need Sphinx and the Read the Docs Theme. These dependencies are automatically taken care of when you
install the package.

.. code-block:: bash

   $ python3.9 -m pip install sphinx sphinx_rtd_theme

You can then create the documentation as follows

.. code-block:: bash

   $ bash scripts/make_docs.sh

**Testing**

There are over 100 tests so far. Both unit tests and integration tests are carried out simultaneously with
no special setup needed.

To run the test suite, simply issue

.. code-block:: bash

   $ pytest -sv tests/

To run a specific test, issue

.. code-block:: bash

   $ pytest -sv tests/test_to_run.py

To run the full coverage suite, we can use

.. code-block:: bash

   $ pytest -sv --cov=algos --cov=algoscli --cov=algosrest --cov-report=html tests/

**Static Analysis and Optimization**

``mypy`` has been used throughout the project. In the vast majority of cases, all variables have been statically
typed, whether interfaces, local variables or class variables.

To perform static analysis for the entire project, one can issue

.. code-block:: bash

   $ mypy algos algoscli algosrest
   Success: no issues found in 13 source files

To perform static analysis for a single file, we can use

.. code-block:: bash

   $ mypy algos/io.py
   Success: no issues found in 1 source file

Due to strictly typing most of the variables, we can gain a quick optimization by using `mypyc` to compile our
code down to Python C extensions. The speed up may range anywhere by up to 4 times, or over while sticking to
standard Python syntax.

Observe the following sequence of steps

.. code-block:: bash

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

**Package Usage**

More can be found in :any:`algos`. The API is separated into groups based on the type of algorithm. An example using the
text module would be to find the anagrams in a given set of words. In python, we could do the following

.. code-block:: bash

   # Generate the input set
   word_set = {'the', 'car', 'can', 'caused', 'a', 'and', 'during', 'cried', 'by', 'its', 'rat', 'bowel', 'drinking',
   'elbow', 'bending', 'that', 'while', 'an', 'thing', 'cider', 'like', 'pain', 'cat', 'which', 'in', 'this',
   'act', 'below', 'is', 'night', 'arc'}

   # Find the anagrams.
   anagrams_found = anagrams(word_set)

   # Sort in order to compare generated anagrams against expected value.
   anagrams_found = [sorted(x) for x in anagrams_found]
   anagrams_found.sort()

   # Print the output
   print(anagrams_found)
   [['act', 'cat'], ['arc', 'car'], ['below', 'bowel', 'elbow'], ['cider', 'cried'], ['night', 'thing']]

**Command Line Usage**

More can be found in :any:`cli` . A small example to get started would be

.. code-block:: bash

   $ echo "below on the elbow is the bowel" | algos-text anagrams | cut -b1-10
   [['below',

The command line interface is made up of command line groupings e.g. ``algos-text``. Within each command line grouping,
there can be a variety of functions. In our case, we are calling the sub-command ``anagrams`` within the ``algos-text``
utility group. The :any:`cli` accepts string input in ``stdin`` and prints to ``stdout`` . The output can be piped
to other utilities and chained indefinitely. A future improvement will be an eval function, that allows python string
representations of data types to be eval'd and used as inputs to the command line algorithms. This would alleviate the
need to convert to and from a plain text representation for each link of the chain.

**REST API Server Usage**

More can be found in :any:`rest_server` . We start the server with the standard ``uvicorn`` usage.

.. code-block:: bash

   $ uvicorn main:app --reload --host 127.0.0.1 --port 8081

If you want to listen for connections outside the localhost, use

.. code-block:: bash

   $ uvicorn main:app --reload --host 0.0.0.0 --port 8081

We can use curl to verify that the server is operational

.. code-block:: bash

   $ curl --header "Content-Type: application/json" \
   --request POST \
   --data '{"input": "below on the elbow is the bowel"}' \
   http://localhost:8081/text/anagrams

   [["bowel","below","elbow"]]

**REST API Client Usage**

More information can be found in :any:`rest_client`. One should start the rest server first. Then, one can perform
single requests or batch requests with the multiprocessing backend.

A single request looks like

.. code-block:: py

   from algosrest.client.request import Request
   req = Request(2, "localhost", 8081)
   result = req.text.anagrams(["elbow below car arc bowel"])
   print(result)
   [[['below', 'elbow', 'bowel'], ['arc', 'car']]]


.. toctree::
   :maxdepth: 3

   algos
   cli
   rest
   tests

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
