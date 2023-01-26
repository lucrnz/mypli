from os import getenv


def validate_auth(headers: dict[str, str]) -> bool:
    return 'KEY' in headers and headers['KEY'] == getenv('SECRET_KEY')
