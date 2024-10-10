#!/bin/sh

# here we replace the environment variables
# provided to the docker container by generating a new temporary file.

python3 -m uvicorn shared.infrastructure.fastapi.main:api --host=0.0.0.0 --reload --port 8080

exec "$@"