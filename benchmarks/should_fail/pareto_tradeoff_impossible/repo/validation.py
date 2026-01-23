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
    print(f"accuracy: {metrics.get('accuracy')}")
    print(f"fairness_gap: {metrics.get('fairness_gap')}")


if __name__ == "__main__":
    main()

