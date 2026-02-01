# Generated Service+Client Benchmark Repo

Entrypoints:
- `python run_server.py` (bootstrap / warmup)
- `python run_client.py` (runs deterministic workload)

Metrics are intentionally *not* printed; they are expected to be emitted to `artifacts/metrics.json`
via Remoroo instrumentation.
