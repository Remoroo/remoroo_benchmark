import json
import os
import subprocess
import sys


def main():
    os.makedirs("artifacts", exist_ok=True)

    # Run train.py once and require metrics.json to exist.
    proc = subprocess.run([sys.executable, "train.py"], capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or "train.py failed")

    path = os.path.join("artifacts", "metrics.json")
    if not os.path.exists(path):
        raise SystemExit("artifacts/metrics.json missing")

    with open(path, "r") as f:
        metrics = json.load(f)

    # Basic sanity: required keys exist.
    for k in ("accuracy", "deterministic"):
        if k not in metrics:
            raise SystemExit(f"missing metric: {k}")

    # Print for stdout regex fallback (engine/judge may use either)
    print(f"accuracy: {metrics.get('accuracy')}")
    print(f"deterministic: {metrics.get('deterministic')}")


if __name__ == "__main__":
    main()

