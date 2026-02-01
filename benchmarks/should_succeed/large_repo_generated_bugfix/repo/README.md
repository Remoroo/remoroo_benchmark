# Generated Large Repo Benchmark

This repo is generated for Remoroo benchmarking.

Entrypoints (multi-command):
- `python run_alpha.py`
- `python run_beta.py`

The application is layered to support system-diagram extraction:
- `cli/` entrypoints
- `services/` orchestration
- `domain/` business logic (intentional bugs live here)
- `infra/` config/logging/utilities
- `adapters/` small interfaces + implementations
