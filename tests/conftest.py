import pytest

from app import create_app, storage


@pytest.fixture
def client():
    """Flask test client, with in-memory storage reset before each test."""
    storage.reset()
    app = create_app(testing=True)
    with app.test_client() as test_client:
        yield test_client
    storage.reset()