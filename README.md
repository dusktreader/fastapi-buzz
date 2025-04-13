[![Latest Version](https://img.shields.io/pypi/v/fastapi-buzz?label=pypi-version&logo=python&style=plastic)](https://pypi.org/project/fastapi-buzz/)
[![Python Versions](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fdusktreader%2Ffastapi-buzz%2Fmain%2Fpyproject.toml&style=plastic&logo=python&label=python-versions)](https://www.python.org/)
[![Build Status](https://github.com/dusktreader/fastapi-buzz/actions/workflows/main.yml/badge.svg)](https://github.com/dusktreader/fastapi-buzz/actions/workflows/main.yml)
[![Documentation Status](https://github.com/dusktreader/fastapi-buzz/actions/workflows/docs.yml/badge.svg)](https://dusktreader.github.io/fastapi-buzz/)

# fastapi-buzz

_py-buzz bindings specifically for FastAPI applications_

This is an extension of the [py-buzz](https://github.com/dusktreader/py-buzz) package.

It adds extra functionality especially for FastAPI. Predominately, it adds the ability to register an error handler with
FastAPI that will automatically package any handled `FastAPIBuzz` exceptions in a nicely formatted JSON response with
the appropriate `status_code` and message. There is also a method to package a FastAPIBuzz error into a response with
some control over what is included in the error body.

## Super-quick Start

Requires: Python 3.10 to 3.13

Install through pip:

```bash
pip install fastapi-buzz
```

Minimal usage example: [examples/basic.py](https://github.com/dusktreader/fastapi-buzz/tree/master/examples/basic.py)


## Documentation

The complete documentation can be found at the
[fastapi-buzz home page](https://dusktreader.github.io/fastapi-buzz)
