#!/bin/sh

# here we replace the environment variables
# provided to the docker container by generating a new temporary file.
envsubst < /app/.env.temp > /app/.env
# then we replace the original env file.
#mv $ASSETS/env.tmp $ASSETS/env.json

#source .venv/bin/activate
#poetry run uvicorn src.shared.infrastructure.fastapi.main:api --host='0.0.0.0' --port 8080 --reload

exec "$@"