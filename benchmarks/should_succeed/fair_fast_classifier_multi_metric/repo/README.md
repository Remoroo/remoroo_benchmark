## Fair + Fast Classifier (Benchmark Repo)

This benchmark repo is intentionally written to be **slow** and **unstable** initially.

- **Entrypoint**: `python train.py`
- **Outputs**: writes `artifacts/metrics.json` with:
  - `accuracy`
  - `loss`
  - `fairness_gap` (absolute accuracy gap between group 0 and group 1)
  - `training_time` (seconds)

The benchmark goal requires improving correctness **and** reducing training time vs baseline.


