#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


/usr/local/bin/gunicorn -b 0.0.0.0:5000 core.wsgi:application -w 4  --bind 0.0.0.0:8000 --chdir=/app

