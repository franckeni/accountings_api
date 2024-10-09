FROM python:3.12-slim AS build

# Set environment variables 
ENV PYTHONDONTWRITEBYTECODE 1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DEFAULT_TIMEOUT=100 PYTHONUNBUFFERED=1

WORKDIR /app
COPY pyproject.toml poetry.lock .env.temp ./

RUN pip install "poetry==1.8.2" \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-root --no-ansi --no-interaction \
    && poetry export -f requirements.txt -o requirements.txt 


### Final stage
FROM python:3.12-slim AS final

ENV APP_HOME=/home/app
WORKDIR $APP_HOME

COPY --from=build /app/requirements.txt /app/.env.temp $APP_HOME/

RUN set -eux \
    groupadd -r fastapi \
    # user non root
    && useradd --no-log-init -r -g fastapi fastapi \
    # 
    && apt-get update \
    && apt-get upgrade -y \
    #
    && apt-get --no-install-recommends install -y curl gettext-base \
    && pip install -r "$APP_HOME"/requirements.txt \
    # 
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

COPY ./src $APP_HOME

# For Ci / CD pipeline env variables
RUN envsubst < "$APP_HOME"/.env.temp > "$APP_HOME"/.env

CMD ["uvicorn", "shared.infrastructure.fastapi.main:api", "--host=0.0.0.0", "--reload", "--port", "8080"]

# Set the default user
USER fastapi