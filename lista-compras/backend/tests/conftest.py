"""
Fixtures para os testes que vocês vão escrever.

Uso típico: def test_algo(client): ...
"""

import pytest

from app import create_app


@pytest.fixture
def app():
    return create_app({"TESTING": True})


@pytest.fixture
def client(app):
    return app.test_client()
