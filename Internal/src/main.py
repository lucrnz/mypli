from os import getenv
from os.path import exists, abspath
from dotenv import load_dotenv
from flask import Flask, Response, request, jsonify
from get_safe_env import get_safe_env
from get_service_path import get_service_path
from process_to_api import process_to_api
from validate_service_path import validate_service_path
from validate_intent import validate_intent

load_dotenv()

app = Flask(__name__)

app.config['DEBUG'] = (getenv('DEBUG') or '0').lower() in ['1', 'true']
services_path = getenv('SRV_PATH') or ''

url_suffix = getenv('URL_SUFFIX') or 'api'
intent_path = getenv('INTENT_PATH') or ''

safe_env = get_safe_env()

if not exists(services_path):
    raise Exception(
        'Environment variable SRV_PATH is not a valid path.')
else:
    services_path = abspath(services_path)

if not exists(intent_path):
    raise Exception(
        'Environment variable INTENT_PATH is not a valid path.')
else:
    intent_path = abspath(intent_path)


def get_unauthorized_response() -> Response:
    app.logger.info('Request not authorized')
    return Response('{err_msg: "Not authorized"}', status=401, mimetype='application/json')


@app.route(f'/{url_suffix}/service/<service>/deploy')
def rebuild_service(service):
    service_path = get_service_path(str(service), services_path)
    (service_path_valid, service_path_response) = validate_service_path(
        service_path, services_path)

    if not service_path_valid and service_path_response != None:
        return service_path_response

    if not validate_intent(request.headers, intent_path):
        return get_unauthorized_response()

    return process_to_api(['bash', 'scripts/deploy.sh'], service_path, safe_env)


if __name__ == '__main__':
    app.run(host=getenv('HOST') or '127.0.0.1', port=getenv('PORT') or '7070')
