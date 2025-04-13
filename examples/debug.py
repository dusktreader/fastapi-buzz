"""
This example shows a basic FastAPI app with a registered error handler for FastAPIBuzz that is running in debug mode.

When you attempt to access the root route, a FastAPIBuzz exception will be raised.
Due to the provided error handler, a nicely formatted error response will be returned.
The response body will include the full message from the handled error (instead of just the `base_message`),
as well as a string representation of the handled error and the response headers.

To run the example, execute this command:

```bash
fastapi dev examples/debug.py
```
"""

from fastapi import FastAPI
from fastapi_buzz import FastAPIBuzz


app = FastAPI()
app.add_exception_handler(*FastAPIBuzz.build_error_handler())
FastAPIBuzz.debug = True


@app.get('/')
def index():
    with FastAPIBuzz.handle_errors("Something went wrong"):
        raise RuntimeError("Boom!")
