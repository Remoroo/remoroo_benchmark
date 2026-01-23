import json
import os
import time

from .pipeline.run import run_job


def main() -> int:
    os.makedirs("artifacts", exist_ok=True)
    t0 = time.time()
    acc = run_job()
    elapsed_s = time.time() - t0

    # Intentionally do NOT print contract metric names.
    # Use aliases + different units to stress baseline extraction.
    elapsed_ms = int(elapsed_s * 1000.0)
    print(f"TOTAL TIME: {elapsed_ms}ms")
    print(f"ACC@1={acc:.4f}")

    # Also write a machine-readable log with non-matching keys.
    with open(os.path.join("artifacts", "run_stats.json"), "w") as f:
        json.dump({"elapsed_ms": elapsed_ms, "acc1": acc}, f, indent=2)

    return 0

