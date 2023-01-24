## api.lucdev.net: Internal API

This code is responsible for managing more sensible tasks such as rebuilding docker containers.

## Configuration

Create a `.env` file

    cp .env.example .env

Add any flag you need to use:

`DEBUG` enables Flask debug mode if set to `1`
`ENV` can be `production` or `development`
`SRV_PATH` should contain the route to the services folder

`GUNICORN_WORKERS` only valid on **production** mode, sets the amount of workers
`GUNICORN_THREADS` only valid on **production** mode, sets the amount of threads

## Build and launch

First make sure you have decent Python version. I am running Python 3.10.9

    python --version

Create a `venv` and activate it:

    python -m venv .venv && source .venv/bin/activate

Install packages

    pip install wheel && pip install -r requirements.txt

Launch the api:

    DEBUG=1 ENV=development ./scripts/launch.sh

Launch the api **production mode**:

    HOST=localhost ./scripts/launch.sh

You may change the .env file to set a custom port
