"""Pytest fixtures for uzbek-translit tests."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from uzbek_translit.api import app


@pytest.fixture
def client() -> Iterator[TestClient]:
    """A FastAPI test client bound to the app."""
    with TestClient(app) as c:
        yield c
