import json
import os
import time


def main():
    os.makedirs("artifacts", exist_ok=True)
    start = time.time()

    # Intentionally slow loop with streaming logs.
    steps = 8
    for i in range(steps):
        # Simulate work
        time.sleep(0.5)
        print(f"progress_step: {i+1}/{steps}")

    runtime_s = time.time() - start
    metrics = {
        "code_runs": True,
        "runtime_s": float(runtime_s),
    }
    with open("artifacts/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print("code_runs: true")
    print(f"runtime_s: {metrics['runtime_s']}")


if __name__ == "__main__":
    main()

