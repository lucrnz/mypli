from flask import jsonify, Response
import subprocess


def process_to_api(process_and_args: list[str], cwd: str, env: dict[str, str]) -> Response:
    cmd = subprocess.run(process_and_args, universal_newlines=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, env=env)
    res = {}
    res["returncode"] = cmd.returncode
    if len(cmd.stdout) > 0:
        res["stdout"] = cmd.stdout
    if len(cmd.stderr) > 0:
        res["stderr"] = cmd.stderr
    res_flask = jsonify(res)
    res_flask.status_code = 500 if cmd.returncode > 0 else 200
    return res_flask
