import json
import os
import random
from typing import Dict, List


def _ensure_dataset(path: str, seed: int = 999, n_rows: int = 7000) -> None:
    """
    Create a deterministic dataset on first run.
    Each row: {"id": int, "text": str, "label": int}
    """
    if os.path.exists(path):
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    rnd = random.Random(seed)
    vocab = [f"w{i}" for i in range(8000)]
    hot = {"w3", "w17", "w88", "w1024"}
    rows: List[Dict[str, object]] = []
    for i in range(n_rows):
        k = 8 + rnd.randint(0, 14)
        toks = [vocab[rnd.randint(0, len(vocab) - 1)] for _ in range(k)]
        label = 1 if any(t in hot for t in toks) else 0
        rows.append({"id": i, "text": " ".join(toks), "label": label})
    with open(path, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


def load_dataset(repo_root: str) -> List[Dict[str, object]]:
    path = os.path.join(repo_root, "data", "dataset.jsonl")
    _ensure_dataset(path)
    out: List[Dict[str, object]] = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out

