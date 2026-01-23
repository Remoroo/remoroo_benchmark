from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from .grid import neighbors4


def plan_a(grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
    # Slow Dijkstra-like search with list scans.
    dist: Dict[Tuple[int, int], int] = {start: 0}
    prev: Dict[Tuple[int, int], Tuple[int, int]] = {}
    visited: List[Tuple[int, int]] = []
    frontier: List[Tuple[int, int]] = [start]

    while frontier:
        # Find node with minimal distance by scanning the full list.
        best = frontier[0]
        best_d = dist.get(best, 10**9)
        for n in frontier:
            d = dist.get(n, 10**9)
            if d < best_d:
                best = n
                best_d = d

        frontier.remove(best)
        visited.append(best)

        if best == goal:
            break

        for nb in neighbors4(best[0], best[1], grid):
            if nb in visited:
                continue
            cand = best_d + 1
            if cand < dist.get(nb, 10**9):
                dist[nb] = cand
                prev[nb] = best
                if nb not in frontier:
                    frontier.append(nb)

    # Reconstruct
    if goal not in dist:
        return []
    path = [goal]
    cur = goal
    while cur != start:
        cur = prev[cur]
        path.append(cur)
    path.reverse()
    return path

