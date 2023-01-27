from json import loads as load_json


def get_host_dir(host_name: str) -> str:
    host_dir = ''
    hosts_txt = ''
    with open('../cfg/hosts.json') as f:
        hosts_txt = f.read()

        hosts = load_json(hosts_txt)

        for host in hosts:
            if host['Name'] == host_name:
                host_dir = host['Services']

        return host_dir
