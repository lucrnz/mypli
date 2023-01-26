from os import remove
from os.path import join, exists


def validate_intent(headers: dict[str, str], intent_path: str) -> bool:
    if not 'INTENT' in headers:
        return False
    if headers['INTENT'] == '':
        return False
    intent_file_path = join(intent_path, headers['INTENT'])
    if exists(intent_file_path):
        remove(intent_file_path)
        return True
    else:
        return False
