import os

import pytest
from fastapi import status
from starlette.testclient import TestClient

from shared.infrastructure.fastapi.main import api


@pytest.fixture(scope="function")
def config_infos():
    """Mocked global configuration for moto."""
    os.environ["version"] = "0.1.0"


@pytest.fixture
def client():

    def title():
        """We provide a title or the test in production will not pass"""

        yield "Testing Accountings API"

    api.dependency_overrides[title] = title

    return TestClient(api)


def test_health_check(client):
    """
    GIVEN
    WHEN health check endpoint is called with GET method
    THEN response with status 200 and body OK is returned
    """
    response = client.get("/health-check")
    version = os.getenv("version", "0.1.0")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "message": f"OK evrything works fine and version is: {version}"
    }
