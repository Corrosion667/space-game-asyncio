"""Main engine of the game."""

import curses
import time

from stars import get_stars
from spaceship import animate_spaceship, fire


def draw(canvas):
    canvas.border()
    canvas.nodelay(True)
    curses.curs_set(False)
    stars = get_stars(canvas)
    max_y, max_x = canvas.getmaxyx()
    start_row = max_y // 2
    start_colunm = max_x // 2
    courutines = [
        *stars,
        fire(canvas, start_row, start_colunm),
        draw_ship(canvas, start_row, start_colunm - 2)
    ]
    while True:
        for courutine in courutines.copy():
            try:
                courutine.send(None)
            except StopIteration:
                courutines.remove(courutine)
        canvas.border()
        canvas.refresh()
        time.sleep(0.1)

def main():
    curses.wrapper(draw)

if __name__ == '__main__':
    main()

