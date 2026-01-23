from __future__ import annotations

import time
from typing import Dict, List, Tuple

from planners import plan_a, plan_b, plan_c
from planners.grid import make_grid


def _run_once(grid, start, goal, fn) -> Tuple[float, int]:
    t0 = time.perf_counter()
    path = fn(grid, start, goal)
    t1 = time.perf_counter()
    return (t1 - t0), len(path)


def run_suite() -> Dict[str, float]:
    grid = make_grid(60, 40)
    start = (1, 1)
    goal = (58, 38)

    # Repeat to reduce noise
    reps = 5
    t_a = 0.0
    t_b = 0.0
    t_c = 0.0
    len_a = 0
    len_b = 0
    len_c = 0
    for _ in range(reps):
        dt, ln = _run_once(grid, start, goal, plan_a)
        t_a += dt
        len_a = ln
        dt, ln = _run_once(grid, start, goal, plan_b)
        t_b += dt
        len_b = ln
        dt, ln = _run_once(grid, start, goal, plan_c)
        t_c += dt
        len_c = ln

    # Use mean runtimes
    planner_a_runtime_s = t_a / reps
    planner_b_runtime_s = t_b / reps
    planner_c_runtime_s = t_c / reps
    runtime_total_s = planner_a_runtime_s + planner_b_runtime_s + planner_c_runtime_s

    # Print minimal deterministic summary (not metrics scraping; just user output).
    print(f"paths: a={len_a} b={len_b} c={len_c}")

    return {
        "planner_a_runtime_s": planner_a_runtime_s,
        "planner_b_runtime_s": planner_b_runtime_s,
        "planner_c_runtime_s": planner_c_runtime_s,
        "runtime_total_s": runtime_total_s,
    }


if __name__ == "__main__":
    _ = run_suite()
