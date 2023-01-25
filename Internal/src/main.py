from os import getenv
from os.path import exists, join, abspath
from flask import Flask, jsonify, Response
from dotenv import load_dotenv
# import subprocess

load_dotenv()

app = Flask(__name__)

app.config['DEBUG'] = (getenv('DEBUG') or '0').lower() in ['1', 'true']
services_path = getenv('SRV_PATH') or ''

if not exists(services_path):
    raise Exception(
        'SRV_PATH is not a valid path. Please check the environment file.')


@app.route('/')
def index():
    return Response("{alive: true}", status=200, mimetype='application/json')


@app.route('/service/<service>/rebuild')
def rebuild_service(service):
    service_path = abspath(join(services_path, str(service)))

    if not service_path.startswith(services_path) or not exists(service_path):
        return Response('{err_msg: "Service not found"}', status=404, mimetype='application/json')

    res = {}
    res['exists'] = True
    return jsonify(res)


if __name__ == '__main__':
    app.run(host=getenv('HOST') or 'localhost', port=getenv('PORT') or '7070')
