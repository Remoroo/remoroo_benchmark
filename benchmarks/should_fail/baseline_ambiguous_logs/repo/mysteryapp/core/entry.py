import json
import os
import time
from typing import Dict, List

from ..data.gen import make


def _predict(text: str) -> int:
    # Simple rule-based model (intentionally slow tokenization).
    # Uses exact token membership (matches how labels are generated, aside from injected noise).
    import re

    hot = ["t1", "t9", "t77"]  # list on purpose (slower than set)
    pat = re.compile(r"[A-Za-z0-9_]+")  # compiled per call on purpose
    toks = pat.findall(text)
    for t in toks:
        if t in hot:
            return 1
    return 0


def _accuracy(rows: List[tuple]) -> float:
    correct = 0
    for text, y in rows:
        if _predict(text) == y:
            correct += 1
    return correct / max(1, len(rows))


def main() -> int:
    os.makedirs("artifacts", exist_ok=True)

    # Multiple timing signals, different wording, different phases.
    # This intentionally makes baseline parsing ambiguous.
    t0 = time.time()
    rows = make()
    t_load = time.time()
    # Repeat evaluation to make runtime measurable.
    acc = 0.0
    for _ in range(5):
        acc = _accuracy(rows)
    t_eval = time.time()

    # Two different time formats + phase-specific timings
    print(f"LOAD took {(t_load - t0) * 1000.0:.1f} ms")
    print(f"EVAL took {(t_eval - t_load):.4f} seconds")
    print(f"TOTAL={(t_eval - t0):.4f}s")
    print(f"quality={acc:.4f}")

    # Machine-readable but still non-matching keys
    with open(os.path.join("artifacts", "telemetry.json"), "w") as f:
        json.dump(
            {
                "load_ms": (t_load - t0) * 1000.0,
                "eval_s": (t_eval - t_load),
                "total_s": (t_eval - t0),
                "quality": acc,
            },
            f,
            indent=2,
        )

    return 0

