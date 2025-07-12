#!/usr/bin/env bash

set -e

# Define a variável FLASK_APP de forma compatível com Flask 2.1
export FLASK_APP=src.app

# Executa as migrações do banco
poetry run flask db upgrade

# Inicia o servidor usando o app dentro da pasta src
poetry run gunicorn src.app:app --bind 0.0.0.0:8000
