"""Main engine of the game."""

import curses
import time

from stars import get_stars
from spaceship import animate_spaceship, fire
from settings import TIC_TIMEOUT, INITIAL_SPACESHIP_POSITION_SHIFT, SPACESHIP_FRAMES
from utils import cycle_object_frames


def draw(canvas):
    """Draw objects on canvas.

    Args:
        canvas: playing field.
    """
    canvas.border()
    canvas.nodelay(True)
    curses.curs_set(False)
    stars = get_stars(canvas)
    ship_frames = cycle_object_frames(SPACESHIP_FRAMES)
    max_row, max_column = canvas.getmaxyx()
    start_row = max_row // 2
    start_colunm = max_column // 2 - INITIAL_SPACESHIP_POSITION_SHIFT
    courutines = [
        *stars,
        fire(canvas, start_row, start_colunm),
        animate_spaceship(canvas, start_row, start_colunm, ship_frames)
    ]
    while True:
        for courutine in courutines.copy():
            try:
                courutine.send(None)
            except StopIteration:
                courutines.remove(courutine)
        canvas.border()
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


def main():
    """Execute game as a script."""
    curses.wrapper(draw)


if __name__ == '__main__':
    main()
