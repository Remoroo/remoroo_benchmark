from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Protocol, Any


class KeyValueStore(Protocol):
    def put(self, key: str, value: Any) -> None: ...
    def get(self, key: str) -> Any: ...


@dataclass
class InMemoryStore:
    data: Dict[str, Any]

    def put(self, key: str, value: Any) -> None:
        self.data[key] = value

    def get(self, key: str) -> Any:
        return self.data.get(key)
