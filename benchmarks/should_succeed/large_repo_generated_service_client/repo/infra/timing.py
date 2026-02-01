from __future__ import annotations

"""Deterministic timing helpers used for 'latency units' style metrics."""

from dataclasses import dataclass
from typing import List

@dataclass
class LatencyTracker:
    samples: List[int]

    def __init__(self):
        self.samples = []

    def add(self, units: int) -> None:
        self.samples.append(int(units))

    def p95(self) -> int:
        if not self.samples:
            return 0
        xs = sorted(self.samples)
        # nearest-rank p95
        idx = int((0.95 * (len(xs) - 1)))
        return xs[idx]
