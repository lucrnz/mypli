## mypli
🚀  API for automatic remote deployment

## Routes

| Route | Method | Description
| --- | --- | --- |
| `/services/{service_name}/pull` | `GET` | This triggers the `pull` action |
| `/services/{service_name}/deploy` | `GET` | This triggers the `deploy` action. |

## What is a service? Where are they?

A service is a folder on your server that holds, usually a git repository.

A service usually has a config for `pulling`, this action usually implies updating to the latest version available. An example would be a git pull.

Another action that a service can have is `deploy`, this action implies updating a service on the server to make it available. Usually implies either restarting some `systemd` service or using a container system such as `docker`.

## Set-up and configuration

Setup environent config and secrets:
	cp .env.example .env

Edit the `.env` file accordingly.

| Variable | Description |
| --- | --- |
| `ENV` | Sets the mode, can be `production` or `development` |
| `HOST` | The host the API listens to |
| `PORT` | The port the API listens to |
| `DEBUG` | Enables Flask debug mode if set to `1` |
| `GUNICORN_WORKERS` | Sets the amount of gunicorn workers |
| `GUNICORN_THREADS` | Sets the amount of gunicorn threads |
| `SECRET_KEY` | A password that you will have to send via a `KEY` header in the `HTTP` request |

Create an SSH key for the service.

This key will be used to connect to hosts, do not add a password to it, when asked for it just press return.

	mkdir -p cfg
	ssh-keygen -t ed25519 -C "api.lucdev.net Agent" -f cfg/key

We need to generate the known_hosts file, for every domain the API will connect:

> ✏️ Do not copy paste! Replace those example domains with your services.

	ssh-keyscan -f cfg/key service-one.myself.tech >> cfg/known_hosts
	ssh-keyscan -f cfg/key -p 2020 service-two.myself.tech  >> cfg/known_hosts
	ssh-keyscan -f cfg/key -p 3050 service-three.myself.tech >> cfg/known_hosts

Do not forget to add the key.pub to the server you are managing.

## Build image and launch

🐳 Use docker.

	docker compose build --no-cache && docker compose up -d
