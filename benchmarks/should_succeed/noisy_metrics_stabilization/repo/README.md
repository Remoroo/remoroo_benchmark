## Noisy Metrics Stabilization

This repo is intentionally nondeterministic:
- `train.py` produces a noisy `accuracy` due to missing seeding.
- It writes `artifacts/metrics.json` with `accuracy` and `deterministic`.

Goal: make the run deterministic and reach `accuracy >= 0.90`.

