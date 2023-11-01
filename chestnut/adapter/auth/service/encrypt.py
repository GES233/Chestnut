import secrets, base64, hashlib
from typing import Callable


def random_char_adpter() -> Callable[[int], bytes]:
    return lambda width: base64.b64encode(secrets.token_bytes(width))


def hash_sha256_adapter() -> Callable[[bytes], bytes]:
    return lambda raw: hashlib.sha256(raw).digest()

