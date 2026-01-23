import json
import os
import time


def evaluate(p: float):
    """
    Coupled metrics (intentional):\n
    - accuracy increases with p\n
    - fairness_gap decreases with p, but we define it as (1 - accuracy)\n
    This makes simultaneously achieving very high accuracy and very low fairness_gap impossible
    beyond the coupling constraint.
    """
    accuracy = max(0.0, min(1.0, p))
    fairness_gap = 1.0 - accuracy
    return accuracy, fairness_gap


def main():
    os.makedirs("artifacts", exist_ok=True)
    start = time.time()

    # Baseline parameter
    p = 0.88
    accuracy, fairness_gap = evaluate(p)

    metrics = {
        "accuracy": float(accuracy),
        "fairness_gap": float(fairness_gap),
        "training_time": float(time.time() - start),
    }
    with open("artifacts/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"accuracy: {metrics['accuracy']}")
    print(f"fairness_gap: {metrics['fairness_gap']}")


if __name__ == "__main__":
    main()

