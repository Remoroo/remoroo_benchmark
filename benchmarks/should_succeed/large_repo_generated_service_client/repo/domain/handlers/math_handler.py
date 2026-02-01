from __future__ import annotations

"""Math handler (intentionally buggy correctness)."""

from typing import List

def sum_numbers(xs: List[int]) -> int:
    return sum(xs)

def mean_numbers(xs: List[int]) -> float:
    # BUG (intentional correctness): uses (n - 1) in denominator.
    if not xs:
        return 0.0
    return sum(xs) / (len(xs) - 1)
