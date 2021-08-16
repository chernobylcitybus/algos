import setuptools
import os
setuptools.setup(
    name='algos',
    version="0.1.0",
    author='Warren Jitsing',
    author_email='warren.jitsing@gmail.com',
    packages=["algos", "algoscli", "algosrest"],
    entry_points={
        'console_scripts': [
            'algos-text=algoscli.main:text',
        ],
    }
)
