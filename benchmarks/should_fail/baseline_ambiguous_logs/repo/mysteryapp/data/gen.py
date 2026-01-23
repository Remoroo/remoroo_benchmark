import random
from typing import List, Tuple


def make(seed: int = 2026, n_rows: int = 45000) -> List[Tuple[str, int]]:
    """
    Deterministic dataset with label noise so that accuracy>=0.90 is unreachable
    for the simple rule-based model used by this repo.
    """
    rnd = random.Random(seed)
    vocab = [f"t{i}" for i in range(5000)]
    hot = {"t1", "t9", "t77"}
    rows: List[Tuple[str, int]] = []
    for _ in range(n_rows):
        k = 10 + rnd.randint(0, 8)
        toks = [vocab[rnd.randint(0, len(vocab) - 1)] for _ in range(k)]
        y = 1 if any(t in hot for t in toks) else 0
        # Inject noise: flip 25% of labels => ceiling ~0.75 for perfect predictor
        if rnd.random() < 0.25:
            y = 1 - y
        rows.append((" ".join(toks), y))
    return rows

