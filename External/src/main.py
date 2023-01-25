from os import getenv, environ
from os.path import exists, join, abspath
from flask import Flask, jsonify, request, Response
from typing import Dict

import subprocess
app = Flask(__name__)

app.config['DEBUG'] = (getenv('DEBUG') or '0').lower() in ['1', 'true']

services_path = getenv('SRV_PATH') or ''

if not exists(services_path):
    raise Exception(
        'Environment variable SRV_PATH is not a valid path.')

if len(getenv('SECRET_KEY') or '') == 0:
    raise Exception(
        'Environment variable SECRET_KEY is not a defined.')

safe_env = environ.copy()

for entry in ['SECRET_KEY', 'SSH_KEY_PRIV', 'SSH_KEY_PUB',
              'SSH_KNOW_HOSTS', 'DEBUG', 'HOST', 'PORT', 'USER_ID', 'GROUP_ID', 'INTERNAL_API_PORT']:
    safe_env.pop(entry, None)


def get_service_path(service_name: str) -> str:
    return abspath(join(services_path, service_name))


def validate_service_path(service_path: str) -> tuple[bool, Response]:
    if not service_path.startswith(services_path) or not exists(service_path):
        return (False, Response('{err_msg: "Service not found"}', status=404, mimetype='application/json'))
    else:
        return (True, None)


def get_unauthorized_response() -> Response:
    app.logger.info('User not authorized')
    return Response('{err_msg: "Not authorized"}', status=401, mimetype='application/json')


def validate_auth(headers: Dict[str, str]) -> bool:
    return headers['KEY'] == getenv('SECRET_KEY')


@app.route('/')
def index():
    meme_url = "https://images7.memedroid.com/images/UPLOADED501/57f66e907bb62.jpeg"
    return f'<html><body><img src="{meme_url}" style="max-width: 100%"/></body></html>'


@app.route('/service/<service>/pull')
def service_pull(service):
    if not validate_auth(request.headers):
        return get_unauthorized_response()

    service_path = get_service_path(str(service))
    (service_path_valid, service_path_response) = validate_service_path(service_path)

    if not service_path_valid and service_path_response != None:
        return service_path_response

    cmd = subprocess.run(["git", "pull", "origin", "main"], universal_newlines=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=service_path, env=safe_env)
    res = {}
    res["returncode"] = cmd.returncode
    if len(cmd.stdout) > 0:
        res["stdout"] = cmd.stdout

    if len(cmd.stderr) > 0:
        res["stderr"] = cmd.stderr
    return jsonify(res)


@app.route('/service/<service>/rebuild')
def service_rebuild(service):
    if not validate_auth(request.headers):
        return get_unauthorized_response()

    service_path = get_service_path(str(service))
    (service_path_valid, service_path_response) = validate_service_path(service_path)

    if not service_path_valid and service_path_response != None:
        return service_path_response

    res = {}
    res['exists'] = True
    return jsonify(res)


if __name__ == '__main__':
    app.run(host=getenv('HOST') or '::', port=getenv('PORT') or '8080')
