#!/bin/bash

. <path/to/src>conf/local/initialize.sh

celery -A ygo_core worker -B -E --loglevel=info