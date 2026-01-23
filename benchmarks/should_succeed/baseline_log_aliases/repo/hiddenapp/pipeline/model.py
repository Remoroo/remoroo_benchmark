from typing import Dict


def predict(counts: Dict[str, int]) -> int:
    hot = ("tok7", "tok42", "tok99", "tok1234")
    s = 0
    for t in hot:
        s += counts.get(t, 0)
    return 1 if s > 0 else 0

