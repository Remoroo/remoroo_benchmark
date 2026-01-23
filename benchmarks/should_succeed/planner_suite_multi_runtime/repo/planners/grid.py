from __future__ import annotations

from typing import Iterable, List, Tuple


def make_grid(width: int, height: int) -> List[List[int]]:
    # 0 = free, 1 = blocked
    g = [[0 for _ in range(width)] for _ in range(height)]
    # Deterministic obstacles (a few diagonal-ish walls)
    for y in range(2, height - 2):
        x = (3 * y) % (width - 2) + 1
        g[y][x] = 1
    for x in range(2, width - 2):
        y = (5 * x) % (height - 2) + 1
        g[y][x] = 1
    return g


def neighbors4(x: int, y: int, grid: List[List[int]]) -> Iterable[Tuple[int, int]]:
    h = len(grid)
    w = len(grid[0]) if h else 0
    if x > 0 and grid[y][x - 1] == 0:
        yield (x - 1, y)
    if x + 1 < w and grid[y][x + 1] == 0:
        yield (x + 1, y)
    if y > 0 and grid[y - 1][x] == 0:
        yield (x, y - 1)
    if y + 1 < h and grid[y + 1][x] == 0:
        yield (x, y + 1)


def manhattan(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

