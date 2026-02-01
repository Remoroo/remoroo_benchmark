from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Settings:
    dataset_name: str = "deterministic_numbers"
    strict_mode: bool = True


def load_settings(dataset_name: Optional[str] = None) -> Settings:
    # Deterministic, no file I/O required.
    if dataset_name:
        return Settings(dataset_name=dataset_name)
    return Settings()
