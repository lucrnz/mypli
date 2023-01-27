import subprocess


def remote_bash(host_name: str, bash_code: str):
    return subprocess.run(['ssh', host_name, 'bash'], universal_newlines=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=bash_code)
