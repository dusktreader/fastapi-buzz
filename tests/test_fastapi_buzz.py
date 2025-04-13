import re
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_buzz import FastAPIBuzz
from tests.conftest import OverloadBuzz


def stripped(text: str):
    """
    Removes all whitespace from a string
    """
    return re.sub(r"\s+", "", text)


class TestFastAPIBuzz:

    def test_raise(self):
        with pytest.raises(FastAPIBuzz, match="i failed"):
            raise FastAPIBuzz("i failed")

    def test_basic_functionality(self, app: FastAPI, client: TestClient):
        """
        This test verifies that the basic functionality of FastAPIBuzz works
        correctly. Verifies that the handler correctly builds a JSONResponse.
        """

        calls: list[tuple[str, Exception]] = []
        def task1(err: Exception):
            calls.append(("task1", err))

        def task2(err: Exception):
            calls.append(("task2", err))

        app.add_exception_handler(*FastAPIBuzz.build_error_handler(task1, task2))

        response = client.get("/")
        assert response.status_code == FastAPIBuzz.status_code
        response_json: dict[str, Any] | None = response.json()
        assert response_json is not None
        assert response_json == dict(
            message="basic test"
        )
        assert [c[0] for c in calls] == ["task1", "task2"]

    def test_debug_mode(self, app: FastAPI, client: TestClient):
        """
        This test verifies that FastAPIBuzz includes error information and uses
        the `base_message` in the response payload when running in debug mode.
        correctly. Verifies that the exception creates a JSONResponse correctly
        when it is bound to an error handler.
        """
        app.add_exception_handler(*FastAPIBuzz.build_error_handler())

        response = client.get("/dangerous")
        assert response.status_code == FastAPIBuzz.status_code
        safe_response_json: dict[str, Any] | None = response.json()
        assert safe_response_json is not None
        assert safe_response_json["message"] == "base message"
        assert "dangerous test" not in safe_response_json["message"]

        try:
            FastAPIBuzz.debug = True
            response = client.get("/dangerous")
        finally:
            FastAPIBuzz.debug = False

        assert response.status_code == FastAPIBuzz.status_code
        debug_response_json: dict[str, Any] | None = response.json()
        assert debug_response_json is not None
        assert debug_response_json["message"] != "base message"
        assert "base message" in debug_response_json["message"]
        assert "dangerous test" in debug_response_json["message"]

    def test_overloaded_status_code(self, app: FastAPI, client: TestClient):
        """
        This test verifies that a derived class builds a JSON response correctly for
        an error handler.
        """
        app.add_exception_handler(*FastAPIBuzz.build_error_handler())

        response = client.get("/status")
        assert response.status_code == 401
        response_json = response.json()
        assert response_json["message"] == "status test"

    def test_derived_handler_does_not_catch_base(self, app: FastAPI, client: TestClient):
        """
        This test verifies that an error handler built from a derived class does not handle
        the base FastAPIBuzz exception.
        """
        app.add_exception_handler(*OverloadBuzz.build_error_handler())

        response = client.get("/status")
        assert response.status_code == 401
        response_json = response.json()
        assert response_json["message"] == "status test"

        with pytest.raises(FastAPIBuzz, match="basic test"):
            response = client.get("/")
