import random
from typing import List, Tuple

from .config import CFG


def make_dataset() -> List[Tuple[str, int]]:
    """
    Deterministic synthetic dataset: (text, label).
    The label depends on presence of certain tokens, so correctness is checkable.
    """
    rnd = random.Random(CFG.seed)
    tokens = [f"tok{i}" for i in range(CFG.vocab_size)]
    hot = {"tok1", "tok7", "tok42", "tok99"}
    rows: List[Tuple[str, int]] = []
    for _ in range(CFG.n_rows):
        k = 10 + rnd.randint(0, 10)
        chosen = [tokens[rnd.randint(0, CFG.vocab_size - 1)] for _ in range(k)]
        # Add some punctuation/noise
        text = " ".join(chosen) + (" !!!" if rnd.random() < 0.1 else "")
        label = 1 if any(t in hot for t in chosen) else 0
        rows.append((text, label))
    return rows

