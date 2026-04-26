from dataclasses import dataclass, asdict, fields
from typing import Optional
import json
from gittchi.paths import config_json


@dataclass
class Config:
    pet_name: str = ""
    pet_type: str = "cat"  # dog, cat, rabbit, bear
    github_username: str = ""
    api_key: str = ""
    model: str = "gemini/gemini-2.5-flash"
    prev_hooks_path: Optional[str] = None


def load_config() -> Config:
    path = config_json()
    if not path.exists():
        return Config()
    data = json.loads(path.read_text(encoding="utf-8"))
    valid = {f.name for f in fields(Config)}
    return Config(**{k: v for k, v in data.items() if k in valid})


def save_config(config: Config) -> None:
    path = config_json()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(config), indent=2, ensure_ascii=False), encoding="utf-8")
    path.chmod(0o600)
