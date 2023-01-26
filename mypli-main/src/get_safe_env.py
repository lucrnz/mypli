from os import environ

def get_safe_env():
    safe_env = environ.copy()

    for entry in ['SECRET_KEY', 'SSH_KEY_PRIV', 'SSH_KEY_PUB',
                'SSH_KNOW_HOSTS', 'DEBUG', 'HOST', 'PORT', 'USER_ID', 'GROUP_ID', 'INTERNAL_API_URL']:
        safe_env.pop(entry, None)
    return safe_env
