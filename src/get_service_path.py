from os.path import join, abspath


def get_service_path(service_name: str, services_path: str) -> str:
    return abspath(join(services_path, service_name))
