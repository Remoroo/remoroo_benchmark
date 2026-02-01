from __future__ import annotations

from dataclasses import dataclass
from typing import List

from adapters.store import KeyValueStore
from domain.data_source import load_record
from domain.alpha.compute import sum_numbers
from infra.logging import get_logger


@dataclass(frozen=True)
class AlphaResult:
    alpha_sum: int


def run_alpha(store: KeyValueStore) -> AlphaResult:
    log = get_logger("alpha_service")
    rec = load_record()
    log.info("loaded_record", n=len(rec.values))
    val = sum_numbers(rec.values)
    store.put("alpha_sum", val)
    return AlphaResult(alpha_sum=val)
