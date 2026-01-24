# Remoroo Performance Benchmarks

This repository contains the official, automated benchmarking suite for the Remoroo Autonomous Experimentation Engine. 

## Overview

The `remoroo_benchmark` system is designed to stress-test autonomous agents across various domains, including algorithmic optimization, environment recovery, and complex refactoring. Each benchmark is executed using the Remoroo CLI, and performance is measured using high-fidelity engineering metrics.

## Key Metrics

- **Success Rate (BSR)**: The percentage of benchmark runs that successfully achieve the research goal.
- **Environment Healing Index (EHI)**: Measures the engine's ability to autonomously repair broken or incomplete development environments.
- **Artifact Replay Fidelity (AFS)**: The degree of determinism in system-state reconstruction during replays.
- **Multi-stage Turn Efficiency**: Average number of turns required to solve complex, multi-step engineering challenges.

## Running Benchmarks

Benchmarks are intended to be run on-demand via GitHub Actions.

```bash
# To run locally (requires Remoroo CLI)
python bench_runner.py --include "should_succeed/*"
```

## Latest Benchmark Results

<!-- BENCHMARK_START -->
| Metric | Value |
| :--- | :--- |
| **Success Rate (BSR)** | 0.0% |
| **Completion Rate** | 0.0% |
| **Total Tests Run** | 1 |

*Last updated: 2026-01-24 21:02:51*
<!-- BENCHMARK_END -->

## Public Leaderboard

The results of the latest benchmark runs are published live to the [Remoroo Engineering Leaderboard](https://www.remoroo.com/).
