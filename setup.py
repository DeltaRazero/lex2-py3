#!/usr/bin/env python

import pathlib as pl
import setuptools

# ***************************************************************************************

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def ReadTxt(fName: str):
    with open(pl.Path(__file__).parent / fName) as f:
        return f.read()

# ***************************************************************************************

import lex2

setuptools.setup(
    name="liblex2-py3",
    version=lex2.__version__,

    packages=setuptools.find_packages(),
    python_requires='>=3.6',

    author="DeltaRazero",
    author_email="deltarazero@gmail.com",
    license="zlib",

    description="Flexible, ruleset-based tokenizer using regex.",
    long_description=ReadTxt("./README.md"),
    long_description_content_type="text/markdown",

    keywords="lexer tokenizer sphinx",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only"
        "Operating System :: OS Independent",

        "License :: OSI Approved :: zlib/libpng License",

        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers"
        "Topic :: Scientific/Engineering :: Information Analysis"
        "Topic :: Software Development :: Compilers",
        "Topic :: Text Processing"
    ],
)
