from enum import Enum
from typing import NamedTuple


class Tile(NamedTuple):
    value: int
    row: int
    col: int


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


Score = int
HighTile = int
