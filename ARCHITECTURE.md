# 2048 Game Architecture

Written by team-lead before spawning teammates. This is the shared blueprint.

## Module Structure

- `src/types/__init__.py`: Type definitions for Tile, Board, Direction, Score
- `src/config/__init__.py`: Game constants (GRID_SIZE=4, WIN_VALUE=2048)
- `src/service/__init__.py`: Core game logic
  - `game.py`: Game class (move, score, high_tile, is_game_over)
  - `board.py`: Board operations (init_grid, slide, merge)
- `src/utils/__init__.py`: Pure helpers
  - `random.py`: Random empty cell selection
  - `display.py`: Text-based grid rendering
- `src/runtime/__init__.py`: Application entry point
  - `app.py`: Wire components, run game loop

## Interfaces

### Types (`src/types/__init__.py`)
- `Tile`: NamedTuple(value: int, row: int, col: int)
- `Direction`: Enum(UP, DOWN, LEFT, RIGHT)
- `Score`: int alias
- `HighTile`: int alias

### Board (`src/service/board.py`)
- `init_board() -> list[list[int]]`: Create 4x4 grid with two starter tiles
- `slide_and_merge(row_or_col: list[int], direction: Direction) -> tuple[list[int], int]`: Slide tiles, merge equals, return new row and score
- `get_column(grid: list[list[int]], col: int) -> list[int]`
- `set_column(grid: list[list[int]], col: int, values: list[int])`

### Game (`src/service/game.py`)
- `Game` class:
  - `__init__()`: Start new game
  - `move(direction: Direction) -> tuple[bool, int]`: Apply move, return (changed, score_delta)
  - `score() -> int`
  - `high_tile() -> int`
  - `is_game_over() -> bool`
  - `grid() -> list[list[int]]`

### Random (`src/utils/random.py`)
- `random_empty_cell(grid: list[list[int]]) -> tuple[int, int] | None`

### Display (`src/utils/display.py`)
- `render_grid(grid: list[list[int]]) -> str`

### Runtime (`src/runtime/app.py`)
- `main() -> None`: Game loop, read input, render

## Shared Data Structures

- Grid: `list[list[int]]` - 4x4 matrix, 0 = empty
- Tile value: powers of 2 (2, 4, 8, 16, ..., 2048+)

## External Dependencies

- Standard library only: `enum`, `random`, `typing`
