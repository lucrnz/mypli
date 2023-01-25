#!/bin/sh
# Warning: use this script from the "Internal" directory, not the ./scripts directory!

if [ ! -f ".env" ]; then
    export ENV="production"
else
    export ENV=$(grep ENV= .env)
fi

if [ "${ENV}" == 'production' ]; then
    python -m gunicorn --chdir src main:app -w $GUNICORN_WORKERS --threads $GUNICORN_THREADS -b $HOST:$PORT
else
    cd src && python main.py
fi
