import inspect
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_buzz import FastAPIBuzz


class OverloadBuzz(FastAPIBuzz):
    status_code: int = 401


def func_name() -> str:
    frame = inspect.currentframe()
    assert frame is not None
    return frame.f_code.co_name


@pytest.fixture
def app():
    app = FastAPI()

    @app.get("/")
    def index():  # pyright: ignore[reportUnusedFunction]
        raise FastAPIBuzz("basic test")

    @app.get("/status")
    def status():  # pyright: ignore[reportUnusedFunction]
        raise OverloadBuzz("status test")

    @app.get("/dangerous")
    def dangerous():  # pyright: ignore[reportUnusedFunction]
        with FastAPIBuzz.handle_errors("base message"):
            raise RuntimeError("dangerous test")

    @app.get("/unhandled")
    def unhandled():  # pyright: ignore[reportUnusedFunction]
        raise RuntimeError("unhandled test")

    return app


@pytest.fixture
def client(app: FastAPI):
    return TestClient(app)
