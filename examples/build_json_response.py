"""
This example shows a basic FastAPI app where the `build_json_response()` method of a `FastAPIBuzz` derived class is
called explicitly.

Note that in addition to the normal fields that are packaged by an error handler, an additional field named "origin" is
included. The `build_json_response()` method can accept arbitrary keyword arguments as long as they are JSON
serializable.

```bash
fastapi dev examples/build_json_response.py
```
"""

from typing import Any
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi_buzz import FastAPIBuzz


app = FastAPI()


class InvalidParameters(FastAPIBuzz):
    status_code: int = status.HTTP_412_PRECONDITION_FAILED


def check_params(id: int | None = None, **_):
    InvalidParameters.require_condition(id, "id field must be defined")


@app.get('/any')
def index(request: Request):
    params: dict[str, Any] = request.query_params
    try:
        check_params(**params)
        return JSONResponse(content=dict(message="All good!"))
    except InvalidParameters as err:
        return err.build_json_response(origin="index")
