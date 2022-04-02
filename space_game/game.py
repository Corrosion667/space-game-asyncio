"""Main engine of the game."""

import curses
import time

from space_game.settings import INITIAL_SPACESHIP_POSITION_SHIFT, SPACESHIP_FRAMES_PATHS, TIC_TIMEOUT
from space_game.spaceship import animate_spaceship, fire
from space_game.stars import get_stars
from space_game.utils import cycle_object_frames


def draw(canvas):
    """Draw objects on canvas.

    Args:
        canvas: playing field.
    """
    canvas.border()
    canvas.nodelay(True)
    curses.curs_set(False)
    stars = get_stars(canvas)
    ship_frames = cycle_object_frames(SPACESHIP_FRAMES_PATHS)
    max_row, max_column = canvas.getmaxyx()
    start_row = max_row // 2
    start_column = max_column // 2
    coroutines = [
        *stars,
        fire(canvas, start_row, start_column),
        animate_spaceship(
            canvas, start_row, start_column - INITIAL_SPACESHIP_POSITION_SHIFT, ship_frames,
        ),
    ]
    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.border()
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


def main():
    """Execute game as a script."""
    curses.wrapper(draw)


if __name__ == '__main__':
    main()
