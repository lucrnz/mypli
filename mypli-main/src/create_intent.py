from uuid import uuid4
from os.path import join


def create_intent(intent_path: str) -> str:
    intent_id = str(uuid4())
    with open(join(intent_path, intent_id), 'w') as new_intent:
        pass
    return intent_id
