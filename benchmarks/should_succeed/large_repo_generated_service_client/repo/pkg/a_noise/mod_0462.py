from __future__ import annotations

"""Noise module 0462 (used for indexing/navigation stress)."""

from dataclasses import dataclass
from typing import List, Dict
from infra.logging import get_logger

VALUE: int = 462

@dataclass(frozen=True)
class NoiseResult:
    module_id: int
    inputs: List[int]
    outputs: List[int]

def transform(x: int) -> int:
    """Deterministic transform."""
    return x + VALUE

def batch_transform(xs: List[int]) -> NoiseResult:
    log = get_logger(f"noise.mod_0462")
    ys = [transform(v) for v in xs]
    log.info("batch_transform", n=len(xs), module_id=VALUE)
    return NoiseResult(module_id=VALUE, inputs=list(xs), outputs=ys)

def summarize(res: NoiseResult) -> Dict[str, int]:
    return {
        "module_id": res.module_id,
        "count": len(res.outputs),
        "min": min(res.outputs) if res.outputs else 0,
        "max": max(res.outputs) if res.outputs else 0,
    }
