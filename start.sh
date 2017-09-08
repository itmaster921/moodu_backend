#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn sync_backend.wsgi:application \
    --bind 0.0.0.0:80 \
    --workers 3 \
    --error-logfile gunicorn_err.log \
    --log-file gunicorn.log \
    --log-config logging.conf

