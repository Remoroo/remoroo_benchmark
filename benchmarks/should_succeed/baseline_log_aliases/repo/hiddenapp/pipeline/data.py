import random
from typing import List, Tuple


def make_dataset(seed: int = 123, n_rows: int = 7000) -> List[Tuple[str, int]]:
    """
    Deterministic synthetic dataset.
    Label is 1 if any of the 'hot' tokens appear.
    """
    rnd = random.Random(seed)
    vocab = [f"tok{i}" for i in range(6000)]
    hot = {"tok7", "tok42", "tok99", "tok1234"}
    rows: List[Tuple[str, int]] = []
    for _ in range(n_rows):
        k = 10 + rnd.randint(0, 12)
        toks = [vocab[rnd.randint(0, len(vocab) - 1)] for _ in range(k)]
        # Add some noise/punct
        txt = " ".join(toks) + (" !!!" if rnd.random() < 0.1 else "")
        y = 1 if any(t in hot for t in toks) else 0
        rows.append((txt, y))
    return rows

