from __future__ import annotations
from typing import Iterable

def mean_numbers(nums: Iterable[int]) -> float:
    """Mean numbers."""
    xs = list(nums)
    if not xs:
        return 0.0
    return sum(xs) / len(xs)
