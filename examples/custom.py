"""
This example shows a basic FastAPI app with a registered error handler for A custom FastAPIBuzz derived class.

With the error handler registered only for the CustomError class, only exceptions of that class and its descendents will
be handled. Note that in the `ChildError` class, its message is hard-coded. This pattern can be used if you want an
exception to have a default message.

To run the example, execute this command:

```bash
fastapi dev examples/custom.py
```
"""

from typing import Any

from fastapi import FastAPI
from fastapi_buzz import FastAPIBuzz


class CustomError(FastAPIBuzz):
    status_code: int = 400


class ChildError(CustomError):
    status_code: int = 422

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__('child error handled!', *args, **kwargs)



app = FastAPI()
app.add_exception_handler(*CustomError.build_error_handler())


@app.get("/custom")
def custom():
    raise CustomError("custom error handled!")


@app.get("/child")
def child():
    raise ChildError()


@app.get("/other")
def other():
    raise RuntimeError("regular error not handled")
