import json
import os
import subprocess
import sys


def main():
    os.makedirs("artifacts", exist_ok=True)
    proc = subprocess.run([sys.executable, "train.py"], capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or "train.py failed")

    path = os.path.join("artifacts", "metrics.json")
    with open(path, "r") as f:
        metrics = json.load(f)

    # Print for stdout regex fallback
    print(f"code_runs: {str(metrics.get('code_runs', False)).lower()}")
    print(f"runtime_s: {metrics.get('runtime_s')}")


if __name__ == "__main__":
    main()

