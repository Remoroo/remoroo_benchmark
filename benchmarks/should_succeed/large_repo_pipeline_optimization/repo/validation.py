import json
import os
import subprocess
import sys


def main():
    os.makedirs("artifacts", exist_ok=True)
    proc = subprocess.run([sys.executable, "main.py"], capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or "main.py failed")

    path = os.path.join("artifacts", "metrics.json")
    if not os.path.exists(path):
        raise SystemExit("artifacts/metrics.json missing")
    with open(path, "r") as f:
        metrics = json.load(f)

    # Print required metrics for stdout fallback
    print(f"runtime_s: {metrics.get('runtime_s')}")
    print(f"correctness: {str(metrics.get('correctness')).lower()}")


if __name__ == "__main__":
    main()

