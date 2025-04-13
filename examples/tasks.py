"""
This example shows a basic FastAPI app with a registered error handler that executes tasks upon activation.

Any time a `FastAPIBuzz` exception (or any descendant classes) is handled, the registered tasks are also executed.
Each task is any callable that accepts a single argument, which will be the handled error.

In this example, every call to the root path will result in the raised error being logged and printed.

```bash
fastapi dev examples/tasks.py
```
"""

import logging

from fastapi import FastAPI
from fastapi_buzz import FastAPIBuzz


logger = logging.getLogger(__name__)


def log_error(err: FastAPIBuzz):
    logger.error(err)


def print_error(err: FastAPIBuzz):
    print(err)


app = FastAPI()
app.add_exception_handler(*FastAPIBuzz.build_error_handler(log_error, print_error))



@app.get('/')
def index():
    raise FastAPIBuzz("There's a problem that should be logged and printed")
