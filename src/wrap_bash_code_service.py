def wrap_bash_code_service(bash_code: str, host_dir: str, service_name: str) -> str:
    return f'cd {host_dir}/{service_name} || exit $?\n{bash_code}'
