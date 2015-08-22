#!/bin/bash

. <path/to/source>/conf/prod/initialize.sh

gunicorn settings.wsgi:application \
    --bind=127.0.0.1:$DJANGO_PORT \
    --workers=$GUNICORN_WORKERS \
    --max-requests 1000 \
    --worker-class eventlet
