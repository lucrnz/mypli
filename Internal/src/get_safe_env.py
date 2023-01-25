from os import environ


def get_safe_env():
    safe_env = environ.copy()

    for entry in ['ENV', 'HOST', 'PORT', 'DEBUG', 'GUNICORN_WORKERS', 'GUNICORN_THREADS', 'SRV_PATH', 'URL_SUFFIX']:
        safe_env.pop(entry, None)
    return safe_env
