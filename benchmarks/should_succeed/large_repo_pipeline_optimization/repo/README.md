## Large Repo Pipeline Optimization

This benchmark is a multi-file, performance-focused repository.

- Entrypoint: `python main.py`
- Metrics output: `artifacts/metrics.json`

The pipeline is intentionally slow due to:
- repeated regex compilation and heavy Python loops
- inefficient membership checks (list instead of dict/set)
- redundant recomputation of intermediate results

Goal: optimize runtime while preserving deterministic correctness.

