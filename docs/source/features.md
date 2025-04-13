# Features

## Error Codes

Each `FastAPIBuzz` exception has a `status_code` class attribute. This should correlate to the type of problem that
happened. For example, the default is the generic `INTERNAL_SERVICE_ERROR` (500). This just means there was a problem in
the application code itself. It is recommended to use different, informative status codes for your different derived
error classes.


## FastAPI compatible `build_json_response()`

In order to make packaging exceptions into normal FastAPI responses easy, this library adds a `build_json_response()`
method. This method composes a FastAPI JSON response with the appropriate `status_code` and the exception message
included in the body.

For example, your route/resource might want to raise a custom exception on certain behaviors and have a response that
informs of the error:

```python
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
```


## Install error handler for FastAPI

The `fastapi-buzz` package also has the ability to set up a FastAPI error handler for `FastAPIBuzz exceptions`. This
allows any code called in the course of request to raise a `FastAPIBuzz` derived exception and have FastAPI
automatically return a properly formatted JSON error response:

```python
app.add_exception_handler(*FastAPIBuzz.build_error_handler())


@app.get("/")
def index():
    raise FastAPIBuzz("Something went wrong")
```

!!! note

    Notice that the unpack/splat (`*`) operator is applied to the return value of `build_error_handler`. This is because
    FastAPI's `register_error_handler` takes two arguments:

      * The type of exception to handle
      * A function that should be passed exception instances when they are caught

    `FastAPIBuzz` returns a tuple that includes:

      * The class type that is being registered
      * A handler function to call


## Adding tasks to error handlers

`FastAPIBuzz` error handlers support adding additional tasks to be executed when a `FastAPIBuzz` exception is handled.
For example, you might wish to log the exceptions before returning the response.

Each task should be a callable that takes exactly one argument: the exception instance itself. These callables are
passed as additional positional arguments:

```python
def log_error(err):
    logger.error(err)

app.add_exception_handler(*FastAPIBuzz.build_error_handler(log_error))
```


## Debug Mode

By default, the error response provided by `FastAPIBuzz` error handlers include the `base_message` for the exception.
This is important only for exceptions raised by the `handle_errors()` (or `check_expressions()`) context manager. This
is because `handle_errors()` includes information about the handled error in its message. The `base_message` does not
include the full message. This is important for production/public apps where you do not wish to expose internal details
to clients.

If you want to get more information in the response to help with debugging, you can enable "Debug Mode" with
`FastAPIBuzz` by setting the class property `debug` to `True`:

```python
FastAPIBuzz.debug = True
```

When that flag is set, the full error message (including any handled error info) is included in the response.
Additionally, a stringified representation of the handled error is also included in the payload. Finally, when "Debug
Mode" is enabled, the response headers are also included in the body.
