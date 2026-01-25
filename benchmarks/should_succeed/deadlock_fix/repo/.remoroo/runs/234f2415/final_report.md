# Run Report: run-1769335000
## ❌ Outcome: PARTIAL_SUCCESS
**Reason**: Early stop: progress stalled after best turn 0 (best_score=180, window_min=180).

## Goal
Fix the deadlock in resource_manager.py. Two threads acquiring resources in different orders causes deadlock.

## Setup & Instrumentation
- No instrumentation patch applied.

## Metrics Evolution
| Metric | Baseline | Turn 0 | Turn 1 | Turn 2 |
|---|---|---|---|---|
| extracted_at | - | 2026-01-25T09:59:20.488313 | 2026-01-25T10:00:12.476884 | 2026-01-25T10:01:06.295006 |
| metrics | - | {'Starting': 10.0, 'doing': 100.0, 'transfers': 1000.0, 'in': 0.51, 'completed_transfers': 820, 'SUCCESS': 820.0, 'runtime_s': 5.8996992111206055} | {'Starting': 10.0, 'doing': 100.0, 'transfers': 1000.0, 'in': 0.51, 'completed_transfers': 820, 'SUCCESS': 820.0, 'runtime_s': 5.916842937469482} | {'Starting': 10.0, 'doing': 100.0, 'transfers': 1000.0, 'in': 1.05, 'completed_transfers': 820, 'SUCCESS': 820.0, 'runtime_s': 5.890751123428345} |
| phase | - | current | current | current |
| run_id | - | run-1769335000 | run-1769335000 | run-1769335000 |
| source | - | merged_repo_artifact+stdout+executor_runtime | merged_repo_artifact+stdout+executor_runtime | merged_repo_artifact+stdout+executor_runtime |
| turn_index | - | 0 | 1 | 2 |

## Turn History
| Turn | Status | Duration |
|---|---|---|
| 0 | SUCCESS | 36.8s |
| 1 | SUCCESS | 46.9s |
| 2 | SUCCESS | 45.6s |