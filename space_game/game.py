import curses
import asyncio
import time
import random

from itertools import cycle
from stars import get_stars


with open('/home/artem/space-game-asyncio/space_game/frames/rocket/rocket_frame_1.txt') as rocket:
    rocket1 = rocket.read()

with open('/home/artem/space-game-asyncio/space_game/frames/rocket/rocket_frame_2.txt') as rocket:
    rocket2 = rocket.read()

iterator = cycle([rocket1, rocket2])

TIC_TIMEOUT = 0.01
BORDER = 1







async def draw_ship(canvas, row, column, symbol):
    while True:
        max_row, max_column = canvas.getmaxyx()
        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        ship = next(symbol)
        frame_rows, frame_columns = get_frame_size(ship)
        if rows_direction > 0:
            row = min(row + rows_direction, max_row-frame_rows - BORDER)
        elif rows_direction < 0:
            row = max(row + rows_direction, 0 + BORDER)
        if columns_direction > 0:
            column = min(column + columns_direction, max_column-frame_columns - BORDER)
        elif columns_direction < 0:
            column = max(column + columns_direction, 0 + BORDER)
        # row = min(row + rows_direction, max_row-frame_rows - BORDER)
        # row = max(row, 0 + BORDER)
        # column = min(column + columns_direction, max_column-frame_columns - BORDER)
        # column = max(column, 0 + BORDER)
        # row = row + rows_direction if rows_direction else row
        # column = column + columns_direction if columns_direction else column
        draw_frame(canvas, row, column, ship, negative=False)
        for _ in range(2):
            await asyncio.sleep(0)
        draw_frame(canvas, row, column, ship, negative=True)



async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


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
        draw_ship(canvas, start_row, start_colunm - 2, iterator)
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

