from flask import jsonify, Response
from subprocess import CompletedProcess

def process_result_to_api(cmd : CompletedProcess[str]) -> Response:
    res = {}
    res["returncode"] = cmd.returncode
    res["stdout"] = cmd.stdout if len(cmd.stdout) > 0 else ''
    res["stderr"] = cmd.stderr if len(cmd.stderr) > 0 else ''
    res_flask = jsonify(res)
    res_flask.status_code = 500 if cmd.returncode > 0 else 200
    return res_flask
