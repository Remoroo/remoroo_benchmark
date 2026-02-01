from __future__ import annotations

from typing import Iterable

def sum_numbers(nums: Iterable[int]) -> int:
    """Sum numbers."""
    xs = list(nums)
    return sum(xs)
