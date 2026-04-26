import os
from gittchi.paths import hmac_key_file


def load_or_create() -> bytes:
    path = hmac_key_file()
    if path.exists():
        return path.read_bytes()
    key = os.urandom(32)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(key)
    path.chmod(0o600)
    return key
