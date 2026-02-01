from __future__ import annotations

from typing import List
from infra.types import Record


def load_numbers() -> List[int]:
    # Deterministic dataset.
    return [1, 2, 3, 4]


def load_record() -> Record:
    return Record(values=load_numbers())
