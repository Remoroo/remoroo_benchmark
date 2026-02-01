from __future__ import annotations

"""Core request/response protocol types."""

from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class Request:
    op: str
    payload: Dict[str, Any]

@dataclass(frozen=True)
class Response:
    ok: bool
    result: Any
    error: str = ""
