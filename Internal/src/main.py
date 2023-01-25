from os import getenv
from os.path import exists, join, abspath
from dotenv import load_dotenv
from flask import Flask, Response
from get_safe_env import get_safe_env
from get_service_path import get_service_path
from process_to_api import process_to_api
from validate_service_path import validate_service_path

load_dotenv()

app = Flask(__name__)

app.config['DEBUG'] = (getenv('DEBUG') or '0').lower() in ['1', 'true']
services_path = getenv('SRV_PATH') or ''
url_suffix = getenv('URL_SUFFIX') or 'api'

safe_env = get_safe_env()


if not exists(services_path):
    raise Exception(
        'SRV_PATH is not a valid path. Please check the environment file.')


@app.route(f'/{url_suffix}')
def index():
    return Response("{alive: true}", status=200, mimetype='application/json')


@app.route(f'/{url_suffix}/service/<service>/deploy')
def rebuild_service(service):
    service_path = get_service_path(str(service), services_path)
    (service_path_valid, service_path_response) = validate_service_path(
        service_path, services_path)

    if not service_path_valid and service_path_response != None:
        return service_path_response

    return process_to_api(['bash', 'scripts/deploy.sh'], service_path, safe_env)


if __name__ == '__main__':
    app.run(host=getenv('HOST') or '127.0.0.1', port=getenv('PORT') or '7070')
