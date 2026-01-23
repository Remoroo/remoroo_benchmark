import json
import os
import random
import time


def compute_accuracy() -> float:
    """
    Simulated evaluation metric.

    Intentionally noisy baseline:
    - No explicit seeding
    - Small random perturbation around a mean that is slightly below target
    """
    mean = 0.88
    noise = random.uniform(-0.06, 0.06)
    acc = mean + noise
    # clamp to [0, 1]
    return max(0.0, min(1.0, acc))


def main():
    os.makedirs("artifacts", exist_ok=True)
    start = time.time()

    acc = compute_accuracy()

    # Heuristic to detect determinism: run twice in-process and compare.
    # This is intentionally weak in the baseline; a correct fix should seed and make runs stable.
    acc2 = compute_accuracy()
    deterministic = abs(acc - acc2) < 1e-12

    metrics = {
        "accuracy": float(acc),
        "deterministic": bool(deterministic),
        "runtime_s": float(time.time() - start),
    }
    with open("artifacts/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"accuracy: {metrics['accuracy']}")
    print(f"deterministic: {metrics['deterministic']}")


if __name__ == "__main__":
    main()

