import json
import os

from math_utils import safe_divide


def main():
    os.makedirs("artifacts", exist_ok=True)
    # This must not crash
    x = safe_divide(10, 0)
    metrics = {"code_runs": True, "safe_divide_result": x}
    with open("artifacts/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    print("code_runs: true")


if __name__ == "__main__":
    main()

