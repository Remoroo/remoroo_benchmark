from __future__ import annotations

"""Lightweight logging primitives (silent by default)."""

import time
from dataclasses import dataclass
from typing import Any, Dict

@dataclass(frozen=True)
class LogEvent:
    ts: float
    level: str
    name: str
    message: str
    fields: Dict[str, Any]

class Logger:
    def __init__(self, name: str):
        self.name = name

    def _emit(self, level: str, message: str, **fields: Any) -> LogEvent:
        return LogEvent(ts=time.time(), level=level, name=self.name, message=message, fields=dict(fields))

    def info(self, message: str, **fields: Any) -> LogEvent:
        return self._emit("INFO", message, **fields)

    def warn(self, message: str, **fields: Any) -> LogEvent:
        return self._emit("WARN", message, **fields)

    def error(self, message: str, **fields: Any) -> LogEvent:
        return self._emit("ERROR", message, **fields)

def get_logger(name: str) -> Logger:
    return Logger(name=name)
