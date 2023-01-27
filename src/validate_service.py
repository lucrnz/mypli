from remote_bash import remote_bash


def validate_service(host_name: str, host_dir: str, service_name: str) -> bool:
    if host_dir == '':
        return False

    cmd = remote_bash(host_name, f'test -d {host_dir}/{service_name}')

    if cmd.returncode != 0 and (len(cmd.stderr) > 0 or len(cmd.stdout > 0)):
        with open('../log.txt', 'a') as log:
            log.write(f'stderr: {cmd.stderr}')
            log.write(f'stdout: {cmd.stdout}')
    return cmd.returncode == 0
