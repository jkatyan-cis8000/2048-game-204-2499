from random import randrange
from typing import Optional


def random_empty_cell(grid: list[list[int]]) -> Optional[tuple[int, int]]:
    """Return a random empty cell (row, col) or None if full."""
    empty = [(r, c) for r in range(4) for c in range(4) if grid[r][c] == 0]
    if not empty:
        return None
    idx = randrange(len(empty))
    return empty[idx]
