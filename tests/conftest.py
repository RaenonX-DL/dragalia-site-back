import pytest

from main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SERVER_NAME"] = "localhost"

    with app.test_client() as client, app.app_context():
        yield client
