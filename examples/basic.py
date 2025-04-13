"""
This example shows a basic FastAPI app with a registered error handler for FastAPIBuzz.

When you attempt to access the root route, a FastAPIBuzz exception will be raised.
Due to the provided error handler, a nicely formatted error response will be returned.

To run the example, execute:

```bash
fastapi dev examples/basic.py
```
"""

from fastapi import FastAPI
from fastapi_buzz import FastAPIBuzz


app = FastAPI()
app.add_exception_handler(*FastAPIBuzz.build_error_handler())


@app.get("/")
def index():
    raise FastAPIBuzz("Something went wrong")
