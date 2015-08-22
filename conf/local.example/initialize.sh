#!/bin/bash

VIRTUALENV_DIR="<path/to/virtualenv>"
SOURCE_DIR="<path/to/source>"
DJANGO_PORT=<django_port>
FLOWER_PORT=<flower_port>

cd $SOURCE_DIR
source "$VIRTUALENV_DIR/bin/activate"

export C_FORCE_ROOT="true"
export DJANGO_SETTINGS_MODULE="settings.local"