from flask import jsonify, Response
from remote_bash import remote_bash

def remote_bash_to_api(bash_code: str, host_name : str, host_dir : str, service_name : str) -> Response:
    cmd = remote_bash(host_name, bash_code=f'cd {host_dir}/{service_name}\n{bash_code}')
    res = {}
    res["returncode"] = cmd.returncode
    if len(cmd.stdout) > 0:
        res["stdout"] = cmd.stdout
    if len(cmd.stderr) > 0:
        res["stderr"] = cmd.stderr
    res_flask = jsonify(res)
    res_flask.status_code = 500 if cmd.returncode > 0 else 200
    return res_flask
