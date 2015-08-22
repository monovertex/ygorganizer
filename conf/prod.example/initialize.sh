#!/bin/bash

VIRTUALENV_DIR="<path/to/virtualenv>"
SOURCE_DIR="<path/to/source>"
CONF_DIR="$SOURCE_DIR/conf/prod"
DJANGO_PORT=<django_port>
GUNICORN_WORKERS=<gunicorn_workers>

cd $SOURCE_DIR
source "$VIRTUALENV_DIR/bin/activate"

export DJANGO_SETTINGS_MODULE="settings.prod"