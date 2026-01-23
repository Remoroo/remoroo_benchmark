from __future__ import annotations

from typing import Dict, List, Tuple

from .grid import manhattan, neighbors4


def plan_b(grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
    # A* with intentionally inefficient open-set handling.
    open_list: List[Tuple[int, int]] = [start]
    came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
    g_score: Dict[Tuple[int, int], int] = {start: 0}
    f_score: Dict[Tuple[int, int], int] = {start: manhattan(start, goal)}

    closed: List[Tuple[int, int]] = []

    while open_list:
        # pick min f by full scan
        current = open_list[0]
        best_f = f_score.get(current, 10**9)
        for n in open_list:
            f = f_score.get(n, 10**9)
            if f < best_f:
                current = n
                best_f = f

        open_list.remove(current)
        closed.append(current)

        if current == goal:
            break

        for nb in neighbors4(current[0], current[1], grid):
            if nb in closed:
                continue
            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(nb, 10**9):
                came_from[nb] = current
                g_score[nb] = tentative_g
                f_score[nb] = tentative_g + manhattan(nb, goal)
                if nb not in open_list:
                    open_list.append(nb)

    if goal not in came_from and goal != start:
        return []
    # reconstruct
    path = [goal]
    cur = goal
    while cur != start:
        cur = came_from[cur]
        path.append(cur)
    path.reverse()
    return path

