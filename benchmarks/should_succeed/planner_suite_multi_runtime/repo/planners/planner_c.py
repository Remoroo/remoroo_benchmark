from __future__ import annotations

from typing import Dict, List, Tuple

from .grid import neighbors4


def plan_c(grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
    # BFS but with inefficient membership checks and queue operations.
    q: List[Tuple[int, int]] = [start]
    prev: Dict[Tuple[int, int], Tuple[int, int]] = {}
    seen: List[Tuple[int, int]] = [start]

    while q:
        cur = q.pop(0)  # O(n)
        if cur == goal:
            break
        for nb in neighbors4(cur[0], cur[1], grid):
            if nb in seen:
                continue
            seen.append(nb)
            prev[nb] = cur
            q.append(nb)

    if goal not in prev and goal != start:
        return []
    path = [goal]
    cur = goal
    while cur != start:
        cur = prev[cur]
        path.append(cur)
    path.reverse()
    return path

