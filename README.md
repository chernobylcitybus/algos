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

