## mypli
🚀  API for automatic remote deployment

[Write up](https://lucdev.net/blog/deployment-tool)

## Routes

| Route | Method | Description
| --- | --- | --- |
| `/{host_name}/{service_name}/{action_name}` | `GET` | This triggers the action `action_name` on the service `service_name`, at the server `host_name`. |

*Note:* Any parameter passed in the query string will be passed to the action as a variable. Read more about it below.

## Response

```json
{
	"returncode": 0,
	"stderr": "Container test-app-api-1  Stopping\nContainer test-app-api-1  Stopping\nContainer test-app-api-1  Stopped\nContainer test-app-api-1  Removing\nContainer test-app-api-1  Removed\nNetwork test-app_default  Removing\nNetwork test-app_default  Removed\n",
	"stdout": ""
}
```

The field `returncode` indicates the status of the command, if it's zero: there were no errors, if it's greater than zero, there were errors.

The fields `stderr` `stdout` contains the output of the command. You may check them for debugging.

## What is a service? Where are they?

A service is a folder on your server that holds, usually a git repository.

A service usually has a config for `pulling`, this action usually implies updating to the latest version available. An example would be a git pull.

Another action that a service can have is `deploy`, this action implies updating a service on the server to make it available. Usually implies either restarting some `systemd` service or using a container system such as `docker`.

Ultimately you as a developer can configure what actions and 

## How to define an actions file

In your service folder, the file `mypli.yml` is excepted.

This file looks like this:

```yaml
pull:
  - git pull origin main

deploy:
  - docker compose down --volumes
  - docker compose build --no-cache
  - docker compose up -d
```

In this case you can replace `pull` with any `action_name`, any command on the list **depends that former command executed correctly**. Any error will stop the pipeline.

You may define as many actions as you need.

*Variables*

You can now define variables in your `mypli.yml` file, for example:

```yaml
pull:
  - git pull origin %var=branch%
```

These variables are loaded from the Query parameters of the request. Make sure to define them in the request, otherwise the command will run with unexcepted results.

## Set-up and configuration

Setup environent config and secrets:
	cp .env.example .env

Edit the `.env` file accordingly.

| Variable | Description |
| --- | --- |
| `HOST` | The host the API listens to |
| `PORT` | The port the API listens to |
| `SECRET_KEY` | A password that you will have to send via a `KEY` header in the `HTTP` request |

Create an SSH key for the service.

This key will be used to connect to hosts, do not add a password to it, when asked for it just press return.

	mkdir -p cfg
	ssh-keygen -t ed25519 -C "api.lucdev.net Agent" -f cfg/key

We need to generate the known_hosts file, for every domain the API will connect:

> ✏️ Do not copy paste! Replace those example domains (and ports) with your services.

	ssh-keyscan -f cfg/key service-one.myself.tech >> cfg/known_hosts
	ssh-keyscan -f cfg/key -p 2020 service-two.myself.tech  >> cfg/known_hosts
	ssh-keyscan -f cfg/key -p 3050 service-three.myself.tech >> cfg/known_hosts

If the above commands don't work for some reason, then try connecting using:

	chmod 600 cfg/key
	ssh user@yourhost -P 3050 -i cfg/key

Then copy your `known_hosts`:

	cp ~/.ssh/known_hosts cfg/known_hosts

Do not forget to add the key.pub to the server you are managing.

## Build image and launch

🐳 Use docker.

	docker compose build --no-cache && docker compose up -d
	
## 🛡️ Security advisory

I am not an expert in software security, run this code in production at your own risk! If you find an exploit to my code **please** let me know, my email address is on my GitHub account.
