#!/bin/bash

. <path/to/src>conf/local/initialize.sh

service nginx restart

find -name '*.pyc' -delete

python "$SOURCE_DIR/manage.py" runserver 0.0.0.0:$DJANGO_PORT
