from pathlib import Path
import os


def home() -> Path:
    base = os.environ.get("GITTCHI_HOME")
    return Path(base) if base else Path.home() / ".gittchi"


def pet_json() -> Path:
    return home() / "pet.json"


def memory_json() -> Path:
    return home() / "memory.json"


def config_json() -> Path:
    return home() / "config.json"


def hmac_key_file() -> Path:
    return home() / ".hmac_key"


def hooks_dir() -> Path:
    return home() / "hooks"


def post_commit_hook() -> Path:
    return hooks_dir() / "post-commit"
