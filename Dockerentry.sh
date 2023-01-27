#!/bin/sh

if [ -d "$HOME/.ssh" ]; then
    rm -rf "$HOME/.ssh"
fi

mkdir -p $HOME/.ssh
cp ./cfg/key $HOME/.ssh/id_ed25519
cp ./cfg/key.pub $HOME/.ssh/id_ed25519.pub
cp ./cfg/known_hosts $HOME/.ssh/known_hosts

python src/generate_ssh_config.py > $HOME/.ssh/config

chmod 700 $HOME/.ssh
chmod 600 $HOME/.ssh/id_ed25519
chmod 644 $HOME/.ssh/id_ed25519.pub
chmod 644 $HOME/.ssh/config
chmod 644 $HOME/.ssh/known_hosts

cat $HOME/.ssh/config

if [ "${ENV}" == 'production' ]; then
    python -m gunicorn --chdir src main:app -w $GUNICORN_WORKERS --threads $GUNICORN_THREADS -b $HOST:$PORT
else
    cd src && python main.py
fi
