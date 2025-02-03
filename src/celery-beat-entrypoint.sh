#!/bin/sh
$counterb
until cd /app/src
do
echo "Waiting for volume to be ready..."
    if [ "$counterb" -gt 3 ];
    then
        echo "Exiting loop!"
        exit 1
    else
        counterb=$((counterb+1))
        sleep 1
    fi
done
celery -A project_celery beat -l info -s /app/src/celerybeat-schedule
