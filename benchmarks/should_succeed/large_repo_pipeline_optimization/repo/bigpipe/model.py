from typing import Dict


def predict(counts: Dict[str, int]) -> int:
    """
    Very simple deterministic classifier:
    - predict 1 if any 'hot' token count is present
    """
    hot = ("tok1", "tok7", "tok42", "tok99")
    s = 0
    for t in hot:
        s += counts.get(t, 0)
    return 1 if s > 0 else 0

