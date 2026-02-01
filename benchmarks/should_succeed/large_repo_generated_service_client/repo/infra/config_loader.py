from __future__ import annotations

"""Config parsing and loading utilities (intentionally inefficient baseline, now optimized)."""

from dataclasses import dataclass
from typing import Dict, Any

_PARSE_CALLS = 0
_CONFIG_CACHE = None

@dataclass(frozen=True)
class Config:
    mode: str
    flags: Dict[str, Any]

def parse_calls() -> int:
    return _PARSE_CALLS

def parse_config(text: str) -> Config:
    """Parse config text.

    This parser should only be called once per server start (after fix).
    """
    global _PARSE_CALLS
    _PARSE_CALLS += 1
    # Simulate 'parsing work' deterministically.
    parts = [p.strip() for p in text.split(",") if p.strip()]
    mode = parts[0] if parts else "default"
    flags = {f"f{i}": (len(p) % 2 == 0) for i, p in enumerate(parts[1:])}
    return Config(mode=mode, flags=flags)

def load_config() -> Config:
    """Load configuration.

    Returns a cached Config object, ensuring parse_config is called only once.
    """
    global _CONFIG_CACHE
    if _CONFIG_CACHE is None:
        text = "prod,alpha,beta,gamma,delta"
        _CONFIG_CACHE = parse_config(text)
    return _CONFIG_CACHE
