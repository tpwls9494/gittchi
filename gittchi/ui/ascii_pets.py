_MOODS: dict[tuple[str, str], str] = {
    ("dog", "happy"):   "(っ≧▽≦)っ",
    ("dog", "neutral"): "( ・ω・)",
    ("dog", "sad"):     "(；ω；)",
    ("dog", "angry"):   "(｀皿´)",
    ("dog", "sick"):    "(x_x )",

    ("cat", "happy"):   "(=^▽^=)♪",
    ("cat", "neutral"): "( =ω=)",
    ("cat", "sad"):     "(=T_T=)",
    ("cat", "angry"):   "(=｀ω´=)",
    ("cat", "sick"):    "(=x_x=)",

    ("rabbit", "happy"):   "(◕ᗜ◕)ノ",
    ("rabbit", "neutral"): "( ◕_◕)",
    ("rabbit", "sad"):     "(◕︿◕)",
    ("rabbit", "angry"):   "(◕益◕)",
    ("rabbit", "sick"):    "(◕_◕;)",

    ("bear", "happy"):   "ʕっ•ᴥ•ʔっ",
    ("bear", "neutral"): " ʕ•ᴥ•ʔ",
    ("bear", "sad"):     "ʕ ᵒ̌ᴥᵒ̌ʔ",
    ("bear", "angry"):   " ʕó㉨òʔ",
    ("bear", "sick"):    " ʕ×_×ʔ",
}

_STATUS_TO_MOOD: dict[str, str] = {
    "최고": "happy", "신남": "happy", "행복": "happy",
    "아픔": "sick",  "위중": "sick",
    "배고픔": "sad", "슬픔": "sad",
    "화남": "angry",
    "보통": "neutral",
}


def get(pet_type: str, status_name: str) -> str:
    mood = _STATUS_TO_MOOD.get(status_name, "neutral")
    return _MOODS.get((pet_type, mood), _MOODS.get((pet_type, "neutral"), "( ・ω・)"))
