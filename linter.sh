#! /bin/bash

#source accounts-type-venv/bin/activate
poetry run black . --exclude '.venv'
poetry run isort . --profile black
poetry run flake8 .