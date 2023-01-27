from os import getenv
from flask import Flask, jsonify, request, Response
from validate_auth import validate_auth
from validate_service import validate_service
from get_host_dir import get_host_dir
from remote_bash_to_api import remote_bash_to_api

app = Flask(__name__)

app.config['DEBUG'] = (getenv('DEBUG') or '0').lower() in ['1', 'true']


if len(getenv('SECRET_KEY') or '') == 0:
    raise Exception(
        'Environment variable SECRET_KEY is not a defined.')


def get_unauthorized_response() -> Response:
    return Response('{err_msg: "Not authorized"}', status=401, mimetype='application/json')


def get_service_not_found_response() -> Response:
    return Response('{err_msg: "Service not found"}', status=404, mimetype='application/json')


@app.route('/<host_name>/<service_name>/pull')
def service_pull(host_name: str, service_name: str):
    if not validate_auth(request.headers):
        return get_unauthorized_response()

    host_dir = get_host_dir(host_name)

    if not validate_service(host_name, host_dir, service_name):
        return get_service_not_found_response()

    return remote_bash_to_api('git pull origin main', host_name, host_dir, service_name)


@app.route('/<host_name>/<service_name>/deploy')
def service_deploy(host_name: str, service_name: str):
    if not validate_auth(request.headers):
        return get_unauthorized_response()

    host_dir = get_host_dir(host_name)

    if not validate_service(host_name, host_dir, service_name):
        return get_service_not_found_response()

    return remote_bash_to_api('./scripts/deploy.sh', host_name, host_dir, service_name)


if __name__ == '__main__':
    app.run(host=getenv('HOST') or '::', port=getenv('PORT') or '7878')
