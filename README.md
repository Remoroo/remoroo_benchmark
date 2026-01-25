# Remoroo Performance Benchmarks

This repository contains the official, automated benchmarking suite for the Remoroo Autonomous Experimentation Engine. 

## Overview

The `remoroo_benchmark` system is designed to stress-test autonomous agents across various domains, including algorithmic optimization, environment recovery, and complex refactoring. Each benchmark is executed using the Remoroo CLI, and performance is measured using high-fidelity engineering metrics.

## Key Metrics

- **Success Rate (BSR)**: The percentage of benchmark runs that successfully achieve the research goal.


## Running Benchmarks

Benchmarks are intended to be run on-demand via GitHub Actions.

```bash
# To run locally (requires Remoroo CLI)
python bench_runner.py --include "should_succeed/*"
```

## Latest Benchmark Results


| Metric | Value |
| :--- | :--- |
| **Success Rate (BSR)** | 95.2% |
| **Total Benchmarks** | 42 |

*Last updated: 2026-01-25 13:53:46*

## Benchmark Results

| Benchmark | Status | Outcome |
| :--- | :---: | :--- |
| baseline_hidden_metrics | ✅ SUCCESS | Correct |
| baseline_log_aliases | ✅ SUCCESS | Correct |
| Cache System Optimization (Multi-Metric) | ✅ SUCCESS | Correct |
| Calculate Mean from CSV | ✅ SUCCESS | Correct |
| Complex Refactor | ✅ SUCCESS | Correct |
| Data Pipeline with Schema Validation | ✅ SUCCESS | Correct |
| EDA Blind Spot (Corrupted Data) | ✅ SUCCESS | Correct |
| Environment Recovery (Env Doctor) | ✅ SUCCESS | Correct |
| Fair + Fast Classifier (Multi-metric, Multi-file) | ✅ SUCCESS | Correct |
| Fair + Fast Classifier (Multi-metric, Multi-file) | ⚠️ PARTIAL_SUCCESS | Correct |
| Fix Cycle Detection in Directed Graph | ✅ SUCCESS | Correct |
| Fix Data Pipeline Aggregation Bug | ✅ SUCCESS | Correct |
| Fix Division Bug | ✅ SUCCESS | Correct |
| Fix Fibonacci Off-by-One | ✅ SUCCESS | Correct |
| Fix Memory Leak in Cache | ✅ SUCCESS | Correct |
| Fix Numerical Instability in Statistics | ✅ SUCCESS | Correct |
| Fix Race Condition in Counter | ✅ SUCCESS | Correct |
| Fix State Machine Transition Bug | ✅ SUCCESS | Correct |
| Fix String Reversal Bug | ✅ SUCCESS | Correct |
| Hard Discovery (Force Search) | ✅ SUCCESS | Correct |
| Hard Multi-stage Hidden Metrics | ✅ SUCCESS | Correct |
| Implement Binary Search Tree | ✅ SUCCESS | Correct |
| Implement Retry Logic with Exponential Backoff | ✅ SUCCESS | Correct |
| Impossible Compression Task | ❌ FAIL | Correct |
| Large Repo Navigation | ✅ SUCCESS | Correct |
| ML Training with Multiple Metrics | ✅ SUCCESS | Correct |
| MNIST Training with PyTorch | ✅ SUCCESS | Correct |
| MNIST Training with PyTorch | ✅ SUCCESS | Correct |
| Noisy Metrics Stabilization (Determinism + Threshold) | ✅ SUCCESS | Correct |
| Patch Brittle Repeated Blocks | ✅ SUCCESS | Correct |
| Performance Optimization | ✅ SUCCESS | Correct |
| Planner Suite Multi-Runtime (Baseline-Relative) | ✅ SUCCESS | Correct |
| Readiness Check | ✅ SUCCESS | Correct |
| Refactor Callback Hell to Async/Await | ✅ SUCCESS | Correct |
| Refactor Circular Import | ✅ SUCCESS | Correct |
| Refactor for Test Coverage | ✅ SUCCESS | Correct |
| Regression Guardrails (Fibonacci) | ✅ SUCCESS | Correct |
| Simpson's Paradox (Causal Inference) | ✅ SUCCESS | Correct |
| Slow Train With Streaming Logs | ✅ SUCCESS | Correct |
| Targeted Ambiguous Date Parsing (Locales) | ✅ SUCCESS | Correct |
| Fix Deadlock in Resource Manager | ⚠️ PARTIAL_SUCCESS | Incorrect |
| Large Repo Pipeline Optimization (Multi-file) | ⚠️ PARTIAL_SUCCESS | Incorrect |


## Public Leaderboard

The results of the latest benchmark runs are published live to the [Remoroo Engineering Leaderboard](https://www.remoroo.com/).
