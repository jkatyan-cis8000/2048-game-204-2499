from typing import List, Tuple
from src.config import constants
from src.types import Direction


def init_board() -> List[List[int]]:
    grid = [[0] * constants.GRID_SIZE for _ in range(constants.GRID_SIZE)]
    grid[0][0] = 2
    grid[0][1] = 2
    return grid


def slide_and_merge(row_or_col: List[int], direction: Direction) -> Tuple[List[int], int]:
    if direction == Direction.LEFT or direction == Direction.UP:
        return _slide_left(row_or_col)
    else:
        return _slide_right(row_or_col)


def _slide_left(row_or_col: List[int]) -> Tuple[List[int], int]:
    filtered = [x for x in row_or_col if x != 0]
    merged = []
    score = 0
    i = 0
    while i < len(filtered):
        if i + 1 < len(filtered) and filtered[i] == filtered[i + 1]:
            new_val = filtered[i] * 2
            merged.append(new_val)
            score += new_val
            i += 2
        else:
            merged.append(filtered[i])
            i += 1
    while len(merged) < constants.GRID_SIZE:
        merged.append(0)
    return merged, score


def _slide_right(row_or_col: List[int]) -> Tuple[List[int], int]:
    filtered = [x for x in row_or_col if x != 0]
    merged = []
    score = 0
    i = len(filtered) - 1
    while i >= 0:
        if i - 1 >= 0 and filtered[i] == filtered[i - 1]:
            new_val = filtered[i] * 2
            merged.append(new_val)
            score += new_val
            i -= 2
        else:
            merged.append(filtered[i])
            i -= 1
    while len(merged) < constants.GRID_SIZE:
        merged.insert(0, 0)
    return merged, score


def get_column(grid: List[List[int]], col: int) -> List[int]:
    return [grid[row][col] for row in range(len(grid))]


def set_column(grid: List[List[int]], col: int, values: List[int]) -> None:
    for row in range(len(grid)):
        grid[row][col] = values[row]
