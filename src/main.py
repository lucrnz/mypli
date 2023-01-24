from os import getenv, getcwd, environ
from os.path import exists
from flask import Flask, jsonify
import subprocess
app = Flask(__name__)

app.config['DEBUG'] = (getenv('DEBUG') or '0').lower() in ['1', 'true']

srv_path = getenv('SRV_PATH') or ''

if not exists(srv_path):
    raise Exception(
        'SRV_PATH is not a valid path. Please check the environment file.')

safe_env = environ.copy()

for entry in ['SECRET_KEY', 'SSH_KEY_PRIV', 'SSH_KEY_PUB',
              'SSH_KNOW_HOSTS', 'DEBUG', 'HOST', 'PORT', 'USER_ID', 'GROUP_ID']:
    safe_env.pop(entry, None)

# Alter home directory, this is needed in the Docker container.
if exists("/.insidedocker"):
    safe_env['HOME'] = getcwd()

@app.route('/')
def index():
    meme_url = "https://images7.memedroid.com/images/UPLOADED501/57f66e907bb62.jpeg"
    return f'<html><body><img src="{meme_url}" style="max-width: 100%"/></body></html>'

@app.route('/deploy/lucsite')
def deploy_lucsite():
    cmd = subprocess.run(["git", "pull", "origin", "main"], universal_newlines=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=f"{srv_path}/lucsite", env=safe_env)
    res = {}
    res["returncode"] = cmd.returncode
    if len(cmd.stdout) > 0:
        res["stdout"] = cmd.stdout

    if len(cmd.stderr) > 0:
        res["stderr"] = cmd.stderr
    return jsonify(res)

if __name__ == '__main__':
    app.run(host=getenv('HOST') or '::', port=getenv('PORT') or '8080')
