#!/bin/bash

. <path/to/source>/conf/prod/initialize.sh

pip install -r "$SOURCE_DIR/requirements.txt"

python "$SOURCE_DIR/manage.py" migrate

python "$SOURCE_DIR/manage.py" collectstatic --noinput \
    -i debug_toolbar \
    -i lib \
    -i src \
    -i templates

find -name '*.pyc' -delete

kill $(cat $VIRTUALENV_DIR/memcached.pid)
memcached -u memcache -d -m <memcached_memory> \
    -s $VIRTUALENV_DIR/memcached.sock \
    -P $VIRTUALENV_DIR/memcached.pid

service nginx restart

supervisorctl restart all