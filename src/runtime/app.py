from src.config import constants
from src.service.game import Game
from src.service.board import init_board
from src.types import Direction
from src.utils.display import render_grid
import sys


def main() -> None:
    game = Game()
    while not game.is_game_over():
        print(render_grid(game.grid()))
        print(f"Score: {game.score()}")
        move_input = _read_move()
        if move_input is None:
            break
        game.move(move_input)
    print(render_grid(game.grid()))
    print(f"Final Score: {game.score()}")
    print("Game Over!")


def _read_move() -> Direction | None:
    try:
        cmd = input("Move (w/a/s/d or q to quit): ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return None
    if cmd == 'q':
        return None
    mapping = {
        'w': Direction.UP,
        'a': Direction.LEFT,
        's': Direction.DOWN,
        'd': Direction.RIGHT,
    }
    return mapping.get(cmd)
