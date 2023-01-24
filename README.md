## api.lucdev.net
🚀  API for managing my personal website/services

## Configuration

Setup environent config and secrets:
	cp .env.example .env

Edit the `.env` file accordingly.

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

	docker compose build --no-cache && docker compose up

## Personal usage

Currently this repo is not publicly avilable so there isn't documentation about it.

I might open source it in the future but currently I have no plans for doing so.
