from typing import Dict


def predict_from_counts(counts: Dict[str, int]) -> int:
    hot = ("w3", "w17", "w88", "w1024")
    s = 0
    for t in hot:
        s += counts.get(t, 0)
    return 1 if s > 0 else 0

