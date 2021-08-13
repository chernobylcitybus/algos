Algos
=====

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

    cd docs/
    make clean && make html

