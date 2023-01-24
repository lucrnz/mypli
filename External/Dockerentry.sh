#!/bin/sh

if [ -d "$HOME/.ssh" ]; then
    rm -rf "$HOME/.ssh"
fi

if [ ! -z "${SSH_KEY_PUB}" ] && [ ! -z "${SSH_KEY_PRIV}" ] && [ ! -z "${SSH_KNOW_HOSTS}" ]; then
    mkdir -vp $HOME/.ssh
    echo $SSH_KEY_PUB | base64 -d > $HOME/.ssh/id_ed25519.pub
    echo $SSH_KEY_PRIV | base64 -d > $HOME/.ssh/id_ed25519
    echo $SSH_KNOW_HOSTS | base64 -d > $HOME/.ssh/known_hosts

    chmod -v 700 $HOME/.ssh
    chmod -v 600 $HOME/.ssh/id_ed25519
    chmod -v 644 $HOME/.ssh/id_ed25519.pub
    chmod -v 644 $HOME/.ssh/known_hosts
fi

if [ "${ENV}" == 'production' ]; then
    python -m gunicorn --chdir src main:app -w $GUNICORN_WORKERS --threads $GUNICORN_THREADS -b $HOST:$PORT
else
    cd src && python main.py
fi
