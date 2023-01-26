## mypli-main

This is the main service, it handles requests 

All tasks will be completed using containers. To manage the containers themselves, the internal API will be called.

## Routes

| Route | Method | Description
| --- | --- | --- |
| `/services/{service_name}/pull` | `GET` | This triggers the `pull` action |
| `/services/{service_name}/deploy` | `GET` | This triggers the `deploy` action. |


## Configuration

Setup environent config and secrets:
	cp .env.example .env

Edit the `.env` file accordingly.

> 💡 **Info**: For PATHS: To go back to the root project folder, use "../" or an absolute path. Keep in mind that all paths are based on this current directory.

| Variable | Description |
| --- | --- |
|  `ENV` | Sets the mode, can be `production` or `development` |
| `HOST` | The host the API listens to |
| `PORT` | The port the API listens to |
| `DEBUG` | Enables Flask debug mode if set to `1` |
| `GUNICORN_WORKERS` | Sets the amount of gunicorn workers |
| `GUNICORN_THREADS` | Sets the amount of gunicorn threads |
| `SRV_PATH` | Contains the route to the services folder |
| `INTENT_PATH` | Path to a shared folder with the external api, used to validate the authenticity of requests |
| `USER_ID` | The id of your user, this has to match the ownership of the `SRV_PATH` and the `INTENT_PATH` |
| `GROUP_ID` | The id of your user group, this has to match the ownership of the `SRV_PATH` and the `INTENT_PATH` |
| `SECRET_KEY` | A password that you will have to send via a `KEY` header in the `HTTP` request |
| `INTERNAL_API_URL` | The `URL` for the internal api, the has to include the suffix. Example: https://my-internal-api.tech/secret-location |
| `SSH_KEY_PRIV` | Your private SSH key for git, base64-encoded, Explained in the section below |
| `SSH_KEY_PUB` | Your public SSH key for git, base64-encoded, Explained in the section below |
| `SSH_KNOW_HOSTS` | The know_hosts file for git, base64-encoded, Explained in the section below |

Create your SSH key.

This key will be used to read from git repos, do not add a password to it, when asked for it press return.

	ssh-keygen -t ed25519 -C "api.lucdev.net Agent" -f key
	echo "SSH_KEY_PRIV=$(base64 -w0 < key)" >> .env
	echo "SSH_KEY_PUB=$(base64 -w0 < key.pub)" >> .env

For `git` to work, we need to generate the know_hosts file, for every domain the API will connect:

	ssh-keyscan -f key github.com >> know_hosts
	ssh-keyscan -f key gitlab.com >> know_hosts
	ssh-keyscan -f key git.mydomain.com >> know_hosts

Now we will encode and embbed this file into the environment file:

	echo "SSH_KNOW_HOSTS=$(base64 -w0 < know_hosts)" >> .env

Don't forget to add the key.pub contents to your git front-end(s).

	echo key.pub

Once you done that, you can delete those files.

	rm key.pub
	rm key
	rm know_hosts


## Build image and launch

Use docker.

	./scripts/launch.sh
