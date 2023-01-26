## mypli-internal

This service is responsible for managing more sensible tasks such as rebuilding docker containers.

It generally has more privileges over the system compared to `main` service.

## Set-up and configuration

Create a `.env` file

    cp .env.example .env

Add or change any flag you need to use:

> 💡 **Info**: Any PATH is relative to the `src` directory, so if you want to go back to the root of the project you will need to do it like this: ../../ or just specify an absolute path.

| Variable | Description |
| --- | --- |
| `DEBUG` | Enables Flask debug mode if set to `1` |
|  `ENV` | Sets the mode, can be `production` or `development` |
| `SRV_PATH` | Contains the route to the services folder |
| `URL_SUFFIX` | Every API endpoint will be prefixed by this. Just adds a bit more of security. |
| `INTENT_PATH` | Path to a shared folder with the external api, used to validate the authenticity of requests |
| `GUNICORN_WORKERS` | Sets the amount of gunicorn workers |
| `GUNICORN_THREADS` | Sets the amount of gunicorn threads |

## Build and launch

First make sure you have decent Python version. I am running Python 3.10.9

    python --version

Create a `venv` and activate it:

    python -m venv .venv && source .venv/bin/activate

Install packages

    pip install wheel && pip install -r requirements.txt

Launch the API:

    ./scripts/launch.sh

**Note**: You should run it as the same user that you are using to manager your docker containers in your VPS.

You may change the .env file to set a custom port, the recommended host is always `localhost` or any that can **only** recieve commands from the *External* API.
