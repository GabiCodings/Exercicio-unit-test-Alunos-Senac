"""Fixtures compartilhadas."""

import pytest

from app import create_app


@pytest.fixture
def app():
    """App Flask sem depender de servidor real (test_client é em memória)."""
    return create_app({"TESTING": True})


@pytest.fixture
def client(app):
    return app.test_client()
