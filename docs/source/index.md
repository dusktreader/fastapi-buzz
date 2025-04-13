# fastapi-buzz

_py-buzz bindings specifically for FastAPI applications_


## Overview

This package extends the functionality from the `py-buzz` package to add some sugar for FastAPI apps.  `FastAPIBuzz`
provides an exception handler builder to create nice error responses with the right status code and information included
in the response body. This means that client code can simply register an error handler with their FastAPI app to supply
fully prepared api responses for specific exception types.

Setting up your FastAPI app to return nicely formatted error responses when FastAPIBuzz exceptions are raised is as
simple as:

```python
app.add_exception_handler(*FastAPIBuzz.build_error_handler())
```

See [examples/basic.py](https://github.com/dusktreader/fastapi-buzz/tree/main/examples/basic.py)
