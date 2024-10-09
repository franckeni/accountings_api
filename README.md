# Install envsubst
apt-get install -y gettext-base

# Run a test
poetry run pytest -v

# Run API
poetry run uvicorn shared.infrastructure.fastapi.main:api --port 8080 --reload

# SONARQUBE
poetry run pytest test/e2e/test.py test/unit/test.py test/integration/test.py --cov=./ --cov-report=xml
pysonar-scanner -Dsonar.token=<your_generated_token>