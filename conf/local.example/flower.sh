#!/bin/bash

. <path/to/src>conf/local/initialize.sh

celery -A ygo_core flower --port=$FLOWER_PORT