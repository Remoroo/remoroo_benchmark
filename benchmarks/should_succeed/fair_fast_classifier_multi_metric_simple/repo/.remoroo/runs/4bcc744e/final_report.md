# Run Report: run-1769279991
## ✅ Outcome: SUCCESS
**Reason**: All required metrics have been satisfied according to the ExperimentContract. The current metrics are: accuracy = 0.905 (>= 0.9), fairness_gap = 0.0307 (<= 0.10), and training_time = 0.1546s (< baseline training_time of 31.56s). These results indicate that the implementation changes have successfully met the goal of improving accuracy, reducing fairness gap, and significantly decreasing training time. No errors were detected during execution, and the command completed successfully.

## Goal
This repo trains a simple binary classifier on a synthetic dataset with two demographic groups. It currently trains slowly (python loops), is unstable (bad learning rate), and produces poor accuracy and an unacceptable fairness gap. Fix the implementation across the codebase so that a single run of `python train.py` writes `artifacts/metrics.json` with ALL required metrics and satisfies: (1) accuracy >= 0.9,  (3) fairness_gap <= 0.10, (3) training_time < baseline training_time. Do not change the metric names. Keep the solution generic and deterministic (seeded).

## Setup & Instrumentation
- No instrumentation patch applied.

## Metrics Evolution
| Metric | Baseline | Turn 0 | Turn 1 |
|---|---|---|---|
| extracted_at | - | 2026-01-24T18:43:41.422188 | 2026-01-24T18:44:33.128545 |
| metrics | - | {'accuracy': 0.8925, 'loss': 0.3907877723208427, 'fairness_gap': 0.015170179903576164, 'training_time': 0.12508702278137207, 'runtime_s': 5.973623991012573} | {'accuracy': 0.905, 'loss': 0.38659360841863166, 'fairness_gap': 0.030740562409719896, 'training_time': 0.1546156406402588, 'runtime_s': 5.967423915863037} |
| phase | - | current | current |
| run_id | - | run-1769279991 | run-1769279991 |
| source | - | merged_repo_artifact+stdout+executor_runtime | merged_repo_artifact+stdout+executor_runtime |
| turn_index | - | 0 | 1 |

## Turn History
| Turn | Status | Duration |
|---|---|---|
| 0 | SUCCESS | 61.4s |
| 1 | SUCCESS | 48.0s |