# Benchmarks

Benchmark test cases for the Remoroo Offline Engine.

## Running Benchmarks

```bash
python -m remoroo_offline.run_benchmark                              # Run all
python -m remoroo_offline.run_benchmark --category should_succeed    # Run category
python -m remoroo_offline.run_benchmark --case ml_training_multi_metric  # Run single case
```

## Current Cases (19 total)

### should_succeed - Single Metric (Easy-Medium)

| Case | Description | Metrics |
|------|-------------|---------|
| `bug_fix` | Fix division by zero | `code_runs == true` |
| `fibonacci_fix` | Fix off-by-one error | `fib_10 == 55` |
| `data_analysis` | Calculate mean from CSV | `mean_value exists` |
| `performance_optimization` | Optimize fibonacci | `execution_time < 1.0` |
| `algorithm_implementation` | Implement BST | `traversal_correct == true` |
| `memory_leak_fix` | LRU cache eviction | `memory_stable == true` |
| `api_client_retry` | Exponential backoff | `retry_works == true` |
| `race_condition_fix` | Thread-safe counter | `completed_transfers == 1000` |

### should_succeed - Single Metric (Hard)

| Case | Description | Metrics |
|------|-------------|---------|
| `multi_file_refactor` | Fix circular import | `code_runs == true` |
| `deadlock_fix` | Fix lock ordering | `completed_transfers == 1000` |
| `floating_point_precision` | Fix numerical instability | `variance_correct == true` |
| `graph_cycle_detection` | Fix false positive cycles | `all_tests_pass == true` |
| `state_machine_bug` | Fix FSM transition bugs | `all_tests_pass == true` |
| `async_refactor` | Callback hell to async/await | `refactor_complete == true` |

### should_succeed - Multi-Metric (Very Hard) 🔥

| Case | Description | Metrics | Artifact |
|------|-------------|---------|----------|
| `ml_training_multi_metric` | Train NN with constraints | `accuracy >= 0.85`, `loss <= 0.5`, `training_time < 30` | `artifacts/metrics.json` |
| `data_pipeline_validation` | ETL with schema validation | `records_processed >= 100`, `null_count == 0`, `schema_valid == true` | `artifacts/validation.json` |
| `code_coverage_refactor` | Fix bugs + achieve coverage | `tests_pass == true`, `coverage >= 80` | `artifacts/coverage.json` |
| `fair_fast_classifier_multi_metric` | Fair + fast classifier | `accuracy >= 0.93`, `loss <= 0.25`, `fairness_gap <= 0.10`, `training_time < baseline training_time` | `artifacts/metrics.json` |
| `noisy_metrics_stabilization` | Noisy metric must be stabilized | `accuracy >= 0.90`, `deterministic == true` | `artifacts/metrics.json` |
| `slow_train_streaming` | Long-running logs | `code_runs == true`, `runtime_s >= 3.0` | `artifacts/metrics.json` |
| `patch_brittle_repeated_blocks` | Patch precision under repeated blocks | `code_runs == true` | `artifacts/metrics.json` |

### should_fail

| Case | Description | Why it should fail |
|------|-------------|-------------------|
| `compression_task` | Compress 50% losslessly | Impossible (information theory) |
| `unreachable_classifier_contract` | Impossible classifier thresholds | Thresholds are intentionally beyond what the toy model can achieve |
| `pareto_tradeoff_impossible` | Conflicting coupled metrics | Requirements conflict by construction (tradeoff cannot satisfy both) |

## Multi-Metric Benchmarks

The **multi-metric** benchmarks are the hardest because:

1. **Multiple constraints must be satisfied simultaneously**
   - `ml_training_multi_metric`: accuracy AND loss AND time
   - `code_coverage_refactor`: tests pass AND coverage threshold

2. **Judge must inspect artifacts**
   - Metrics are stored in JSON files, not just stdout
   - Judge needs to parse and evaluate artifact contents

3. **Tradeoffs between metrics**
   - Optimizing one metric may hurt another
   - Requires balanced solutions

## Artifact-Based Evaluation

For complex benchmarks, the Judge evaluates by:
1. Reading `artifacts/*.json` files
2. Parsing metric values from structured data
3. Comparing against thresholds

Example `artifacts/metrics.json`:
```json
{
  "accuracy": 0.87,
  "loss": 0.42,
  "training_time": 25.3
}
```

## Difficulty Guide

| Level | Characteristics | Expected Turns |
|-------|-----------------|----------------|
| **Easy** | Single file, single metric, obvious fix | 1-2 |
| **Medium** | Single metric, requires understanding | 2-4 |
| **Hard** | Multi-file or subtle bug, single metric | 4-8 |
| **Very Hard** | Multiple metrics, artifact inspection, tradeoffs | 8-12 |
