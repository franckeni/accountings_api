from pathlib import Path

import pytest
from dotenv import load_dotenv


if Path(".env.test").exists():
    load_dotenv(dotenv_path=(Path(".env.test")))
elif Path(".env.dev").exists():
    load_dotenv(dotenv_path=(Path(".env.dev")))
else:
    load_dotenv(".env")

from fastapi import status
from moto import mock_aws
from starlette.testclient import TestClient

from shared.infrastructure.fastapi.main import api
from shared.infrastructure.fastapi.settings import Settings

# Get the global configuration
config = Settings()


@pytest.fixture
def client():
    return TestClient(api)


def test_health_check(client):
    """
    GIVEN
    WHEN health check endpoint is called with GET method
    THEN response with status 200 and body OK is returned
    """
    response = client.get("/health-check")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "message": f"OK evrything works fine and version is: {config.version}"
    }
