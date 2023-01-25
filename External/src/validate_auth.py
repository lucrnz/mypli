from os import getenv


def validate_auth(headers: dict[str, str]) -> bool:
    return headers['KEY'] == getenv('SECRET_KEY')
