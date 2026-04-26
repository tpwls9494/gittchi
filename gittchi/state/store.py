import hmac as _hmac
import hashlib
import json
from pathlib import Path
from gittchi.state.hmac_key import load_or_create


class TamperedError(Exception):
    pass


def _sign(data_bytes: bytes, key: bytes) -> str:
    return _hmac.new(key, data_bytes, hashlib.sha256).hexdigest()


def _verify(data_bytes: bytes, sig: str, key: bytes) -> bool:
    expected = _hmac.new(key, data_bytes, hashlib.sha256).hexdigest()
    return _hmac.compare_digest(expected, sig)


def _serialize(data: dict) -> bytes:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def load(path: Path) -> dict | None:
    """None = 파일 없음. TamperedError = 서명 불일치."""
    if not path.exists():
        return None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        key = load_or_create()
        data_bytes = _serialize(raw["data"])
        if not _verify(data_bytes, raw["sig"], key):
            path.unlink(missing_ok=True)  # 변조 파일 삭제
            raise TamperedError(path.name)
        return raw["data"]
    except TamperedError:
        raise
    except Exception:
        return None  # 손상된 파일 → 없는 것으로 처리


def save(path: Path, data: dict) -> None:
    key = load_or_create()
    data_bytes = _serialize(data)
    sig = _sign(data_bytes, key)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"data": data, "sig": sig}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    path.chmod(0o600)
