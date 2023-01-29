from os import getenv
from flask import Flask, jsonify, request, Response
from validate_auth import validate_auth
from validate_service import validate_service
from get_host_dir import get_host_dir
from process_result_to_api import process_result_to_api
from remote_bash import remote_bash
from wrap_bash_code_service import wrap_bash_code_service
from subprocess import CompletedProcess
from yaml import safe_load as yaml_load

app = Flask(__name__)

app.config['DEBUG'] = (getenv('DEBUG') or '0').lower() in ['1', 'true']


if len(getenv('SECRET_KEY') or '') == 0:
    raise Exception(
        'Environment variable SECRET_KEY is not a defined.')


def json_err_msg(msg: str) -> str:
    return '{"returncode": 1, "err_msg": "' + msg + '"}'


def get_unauthorized_response() -> Response:
    return Response(json_err_msg("Not authorized"), status=401, mimetype='application/json')


def get_invalid_request_response() -> Response:
    return Response(json_err_msg("Invalid request"), status=400, mimetype='application/json')


def get_service_not_found_response() -> Response:
    return Response(json_err_msg("Service not found"), status=404, mimetype='application/json')


def get_service_invalid_yml() -> Response:
    return Response(json_err_msg("Service mypli.yml not found"), status=404, mimetype='application/json')


def get_service_invalid_action(action_name: str) -> Response:
    res = {}
    res['err_msg'] = f"Service action {action_name} not found"
    res_flask = jsonify(res)
    res_flask.status_code = 404
    return res_flask


def validate_input(input_data: str) -> bool:
    return not any(c in "!@#$%^&*()+?=,<>/;\'\"" for c in input_data)


@app.route('/<host_name>/<service_name>/<action_name>')
def service_pull(host_name: str, service_name: str, action_name: str):
    if not validate_auth(request.headers):
        return get_unauthorized_response()

    if not validate_input(host_name) or not validate_input(service_name) or not validate_input(action_name):
        return get_invalid_request_response()

    host_dir = get_host_dir(host_name)

    if not validate_service(host_name, host_dir, service_name):
        return get_service_not_found_response()

    code = wrap_bash_code_service('cat mypli.yml', host_dir, service_name)
    cmd_file: CompletedProcess[str] = remote_bash(host_name, code)

    if cmd_file.returncode != 0 or len(cmd_file.stdout) == 0:
        return get_service_invalid_yml()

    service_def = yaml_load(cmd_file.stdout)

    if not action_name in service_def:
        get_service_invalid_action(action_name)

    code = wrap_bash_code_service(' && '.join(
        service_def[action_name]), host_dir, service_name)
    return process_result_to_api(remote_bash(host_name, code))


if __name__ == '__main__':
    app.run(host=getenv('HOST') or '::', port=getenv('PORT') or '7878')
