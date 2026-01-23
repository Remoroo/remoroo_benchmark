import json
import os
import time

from bigpipe.pipeline import run_pipeline


def main():
    os.makedirs("artifacts", exist_ok=True)
    t0 = time.time()
    result = run_pipeline()
    runtime_s = time.time() - t0

    metrics = {
        "runtime_s": float(runtime_s),
        "correctness": bool(result["correctness"]),
        "checksum": result["checksum"],
        "num_rows": result["num_rows"],
    }
    with open("artifacts/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    # stdout fallback
    print(f"runtime_s: {metrics['runtime_s']}")
    print(f"correctness: {str(metrics['correctness']).lower()}")


if __name__ == "__main__":
    main()

