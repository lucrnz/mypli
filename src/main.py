from os import getenv
from os.path import exists, abspath
from flask import Flask, jsonify, request, Response
from get_safe_env import get_safe_env
from get_service_path import get_service_path
from process_to_api import process_to_api
from validate_auth import validate_auth
from validate_service_path import validate_service_path
from create_intent import create_intent

import requests
import subprocess
app = Flask(__name__)

app.config['DEBUG'] = (getenv('DEBUG') or '0').lower() in ['1', 'true']

if len(getenv('SECRET_KEY') or '') == 0:
    raise Exception(
        'Environment variable SECRET_KEY is not a defined.')

safe_env = get_safe_env()


def get_unauthorized_response() -> Response:
    app.logger.info('Request not authorized')
    return Response('{err_msg: "Not authorized"}', status=401, mimetype='application/json')

@app.route('/<hostname>/<service>/pull')
def service_pull(hostname, service):
    if not validate_auth(request.headers):
        return get_unauthorized_response()

    service_path = get_service_path(str(service), services_path)
    (service_path_valid, service_path_response) = validate_service_path(
        service_path, services_path)

    if not service_path_valid and service_path_response is not None:
        return service_path_response

    return process_to_api(['git', 'pull', 'origin', 'main'], service_path, safe_env)


@app.route('/<hostname>/<service>/deploy')
def service_deploy(hostname : str, service : str):
    if not validate_auth(request.headers):
        return get_unauthorized_response()

    service_path = get_service_path(str(service), services_path)
    (service_path_valid, service_path_response) = validate_service_path(
        service_path, services_path)

    if not service_path_valid and service_path_response != None:
        return service_path_response

    err_response: Response | None = None
    api_response: requests.Response | None = None
    intent_id = create_intent(intent_path)

    try:
        api_response = requests.get(
            f"{getenv('INTERNAL_API_URL')}/service/{service}/deploy", headers={'INTENT': intent_id})
    except BaseException as e:
        json_dict = {}
        json_dict["err_msg"] = f"Internal API error: {e}"
        err_response = jsonify(json_dict)
        err_response.status_code = 500
    finally:
        if err_response is None and api_response is not None:
            return Response(api_response.text, api_response.status_code, None, None, api_response.headers['content-type'])
        else:
            return err_response


if __name__ == '__main__':
    app.run(host=getenv('HOST') or '::', port=getenv('PORT') or '7878')
