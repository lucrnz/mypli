from os import getenv
from os.path import exists
from flask import Flask, jsonify
from dotenv import load_dotenv
# import subprocess

load_dotenv()

app = Flask(__name__)

app.config['DEBUG'] = (getenv('DEBUG') or '0').lower() in ['1', 'true']
srv_path = getenv('SRV_PATH') or ''

if not exists(srv_path):
    raise Exception(
        'SRV_PATH is not a valid path. Please check the environment file.')

@app.route('/')
def index():
    res = {}
    res['alive'] = True
    return jsonify(res)
