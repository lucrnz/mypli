from flask import Response
from os.path import exists


def validate_service_path(service_path: str, services_path: str) -> tuple[bool, Response]:
    folder_exists = exists(service_path)
    folder_within_path = service_path.startswith(services_path)
    folder_is_not_same = service_path is not services_path

    if folder_exists and folder_within_path and folder_is_not_same:
        return (True, None)
    else:
        return (False, Response('{err_msg: "Service not found"}', status=404, mimetype='application/json'))
