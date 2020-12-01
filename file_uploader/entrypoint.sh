#!/usr/bin/env bash

set -o errexit
set -o pipefail

# set -o nounset

cmd="$@"

function elastic_ready() {
    response=$(
        curl --write-out %{http_code} --silent --output /dev/null elasticsearch:9200/_cluster/health?wait_for_status=yellow &
        timeout=50s
    )
    if [ $response -ge 200 ]; then
        return 0
    else
        return -1
    fi
}

until elastic_ready; do
    echo >&2 "Elastic is unavailable - sleeping"
    sleep 1
done
echo >&2 "Elastic is up - continuing..."

function mysql_ready() {

    mysqladmin -h mysql -uroot -p$MYSQL_ROOT_PASSWORD processlist

    if [ $? -eq 0 ]; then
        return 0
    else
        return -1
    fi
}
until mysql_ready; do
    echo >&2 "Mysql is unavailable - sleeping"
    sleep 1
done
echo >&2 "Mysql is up - continuing..."
python manage.py makemigrations
python manage.py migrate

if [ -z "$cmd" ]; then
    if [ "x$localdev" = "xtrue" ]; then
        exec python main.py run -h 0.0.0.0
    else
        exec /app/gunicorn.sh
    fi
else
    exec $cmd
fi
