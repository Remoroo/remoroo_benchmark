# Run Report: run-1769302257
## ✅ Outcome: SUCCESS
**Reason**: All required metrics have been significantly improved compared to the baseline, achieving reductions of over 96% in runtime for all planners and the total runtime. The experiment's goal to optimize the runtime of the planners without changing outputs has been successfully met, as evidenced by the metrics extracted from the current execution. No errors were detected, and all commands executed successfully, satisfying the ExperimentContract's requirements for success.

## Goal
Optimize the runtime of the planners without changing outputs.

## Setup & Instrumentation
- No instrumentation patch applied.

## Metrics Evolution
| Metric | Baseline | Turn 0 | Turn 1 | Turn 2 |
|---|---|---|---|---|
| extracted_at | - | 2026-01-25T00:52:33.266603 | 2026-01-25T00:53:19.024788 | 2026-01-25T00:54:26.277479 |
| metrics | - | {'a': 95.0, 'b': 95.0, 'c': 95.0, 'planner_a_runtime_s': 0.07972703340346925, 'planner_b_runtime_s': 0.07726811679895036, 'planner_c_runtime_s': 0.07456771659199149, 'runtime_total_s': 0.2315628667944111, 'runtime_s': 5.803993225097656} | {'a': 95.0, 'b': 95.0, 'c': 95.0, 'planner_a_runtime_s': 0.07840065839700401, 'planner_b_runtime_s': 0.0778316084004473, 'planner_c_runtime_s': 0.07460100819007494, 'runtime_total_s': 0.23083327498752626, 'runtime_s': 5.869211196899414} | {'a': 95.0, 'b': 95.0, 'c': 95.0, 'planner_a_runtime_s': 0.0022813999967183918, 'planner_b_runtime_s': 0.002655950404005125, 'planner_c_runtime_s': 0.0013328000030014664, 'runtime_total_s': 0.0062701504037249835, 'runtime_s': 5.286742925643921} |
| phase | - | current | current | current |
| run_id | - | run-1769302257 | run-1769302257 | run-1769302257 |
| source | - | merged_repo_artifact+stdout+executor_runtime | merged_repo_artifact+stdout+executor_runtime | merged_repo_artifact+stdout+executor_runtime |
| turn_index | - | 0 | 1 | 2 |

## Turn History
| Turn | Status | Duration |
|---|---|---|
| 0 | SUCCESS | 32.7s |
| 1 | SUCCESS | 40.3s |
| 2 | SUCCESS | 58.1s |