from __future__ import annotations

from dataclasses import dataclass

from adapters.store import KeyValueStore
from domain.data_source import load_record
from domain.beta.stats import mean_numbers
from infra.logging import get_logger


@dataclass(frozen=True)
class BetaResult:
    beta_mean: float


def run_beta(store: KeyValueStore) -> BetaResult:
    log = get_logger("beta_service")
    rec = load_record()
    log.info("loaded_record", n=len(rec.values))
    val = mean_numbers(rec.values)
    store.put("beta_mean", val)
    return BetaResult(beta_mean=val)
