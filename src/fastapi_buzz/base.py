from __future__ import annotations

from functools import partial
from typing import Any, Callable, TypeAlias, cast
from typing_extensions import Self, override

from fastapi import status, Request
from fastapi.responses import Response, JSONResponse
from starlette.types import HTTPExceptionHandler
from buzz import Buzz


FastAPIBuzzTask: TypeAlias = Callable[["FastAPIBuzz"], None]
"""A function that takes a FastAPIBuzz exception and performs a task on it"""


class FastAPIBuzz(Buzz):
    # These are the values that should be used by default when this exception is handled by a faastapi error handler
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    headers: dict[str, str] | None = None

    # If set, additional error information will be included in error
    # produced by error handlers.
    debug: bool = False

    @override
    def __str__(self):
        return "{super_str} ({status_code})".format(
            super_str=super().__str__(),
            status_code=self.status_code,
        )

    def build_json_response(
        self,
        status_code: int | None = None,
        message: str | None = None,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> JSONResponse:
        """
        Build a json response from the FastAPI error in form that is compatible with FastAPI.

        Keyword arguments allow custom data to be included in the rsponse's body when it is built.

        If `debug` is set, the stringified exception will be included in the response body as well. For apps running
        in production or publicly should not run in debug mode as this could expose internal information to clients.

        Args:

            status_code: The status code to include in the response. If not supplied, use instance status_code.
            message:     The message to include in the response. If not supplied, use instance message. If debug
                         is set and the base_message is not None, use the base_message instead. This is important,
                         because if the exception was raised by `handle_errors`, the full message will return
                         details of the handled exception as well as the base message. This information should
                         probably not be returned to the client.
            headers:     The headers to attach to the response. If not supplied, use instance headers. If the
                         instance has no headers, don't include headers.
            kwargs:      Additional fields that should be set in the response body. These must be JSON
                         serializable.
        """
        if status_code is None:
           status_code = self.status_code
        if message is None:
            if not self.debug and self.base_message is not None:
                message = self.base_message
            else:
                message = self.message
        if headers is None and self.headers is not None:
            headers = self.headers
        else:
            headers = {}

        content: dict[str, Any] = dict(
            message=message,
            **kwargs,
        )

        if self.debug:
            content.update(
                error=str(self),
                headers=headers,
            )

        return JSONResponse(
            status_code=status_code,
            headers=headers,
            content=content,
        )

    @classmethod
    def build_error_handler(cls, *tasks: FastAPIBuzzTask) -> tuple[type[Self], HTTPExceptionHandler]:
        """
        Build an error handling function specifically for FastAPIBuzz errors.

        The resulting error handler function will catch any FastAPIBuzz exceptions and raise an HTTPException that
        encapsulates the details of the original.

        Descendants of the exception will also be caught and handled.

        Example usage:

        ```python
        app.add_exception_handler(*FastAPIBuzz.build_error_handler())
        ```

        You may also add extra tasks that will operate on the error prior raising the final HTTPException:

        ```python
        app.register_error_handler(*FastAPIBuzz.build_error_handler(print, lambda e: jawa(e)))
        ```

        This latter example will print the error to stdout and also call the `jawa()` function with the error prior to
        raising the final HTTPException.
        """

        def _handler(*args: FastAPIBuzzTask| Request | Self) -> Response:
            _tasks: list[FastAPIBuzzTask] = [cast(FastAPIBuzzTask, t) for t in args[:-2]]
            _: Request = cast(Request, args[-2])
            error: Self = cast(Self, args[-1])
            for task in _tasks:
                task(error)
            return error.build_json_response()

        return (cls, partial(_handler, *tasks))
