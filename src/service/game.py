from typing import List, Tuple
from src.types import Direction, Score, HighTile
from src.config import constants
from src.service import board


class Game:
    def __init__(self) -> None:
        self._grid: List[List[int]] = board.init_board()
        self._score: Score = 0
        self._high_tile: HighTile = 2

    def move(self, direction: Direction) -> Tuple[bool, int]:
        changed = False
        score_delta = 0

        if direction in (Direction.LEFT, Direction.RIGHT):
            for row in range(constants.GRID_SIZE):
                new_row, row_score = board.slide_and_merge(
                    self._grid[row][:], direction
                )
                if new_row != self._grid[row]:
                    changed = True
                    self._grid[row] = new_row
                    score_delta += row_score
        else:
            for col in range(constants.GRID_SIZE):
                col_values = board.get_column(self._grid, col)
                new_col, col_score = board.slide_and_merge(col_values, direction)
                if new_col != col_values:
                    changed = True
                    board.set_column(self._grid, col, new_col)
                    score_delta += col_score

        if changed:
            self._score += score_delta
            self._update_high_tile()

        return changed, score_delta

    @property
    def score(self) -> Score:
        return self._score

    @property
    def high_tile(self) -> HighTile:
        return self._high_tile

    def is_game_over(self) -> bool:
        for row in range(constants.GRID_SIZE):
            for col in range(constants.GRID_SIZE):
                if self._grid[row][col] == 0:
                    return False
        return True

    @property
    def grid(self) -> List[List[int]]:
        return self._grid[:]

    def _update_high_tile(self) -> None:
        max_val = 0
        for row in self._grid:
            for val in row:
                if val > max_val:
                    max_val = val
        self._high_tile = max_val
