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


SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258


def read_controls(canvas):
    """Read keys pressed and returns tuple witl controls state."""

    rows_direction = columns_direction = 0
    space_pressed = False

    while True:
        pressed_key_code = canvas.getch()

        if pressed_key_code == -1:
            # https://docs.python.org/3/library/curses.html#curses.window.getch
            break

        if pressed_key_code == UP_KEY_CODE:
            rows_direction = -1

        if pressed_key_code == DOWN_KEY_CODE:
            rows_direction = 1

        if pressed_key_code == RIGHT_KEY_CODE:
            columns_direction = 1

        if pressed_key_code == LEFT_KEY_CODE:
            columns_direction = -1

        if pressed_key_code == SPACE_KEY_CODE:
            space_pressed = True

    return rows_direction, columns_direction, space_pressed


async def draw_ship(canvas, row, column, symbol):
    while True:
        max_row, max_column = canvas.getmaxyx()
        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        ship = next(symbol)
        # if rows_direction > 0:
        #     row = min(row + rows_direction, max_row - BORDER)
        # elif rows_direction < 0:
        #     row = max(row + rows_direction, 0 + BORDER)
        # if columns_direction > 0:
        #     column = min(column + columns_direction, max_column - BORDER)
        # elif columns_direction < 0:
        #     column = max(column + columns_direction, 0 + BORDER)
        row = min(row + rows_direction, max_row - BORDER)
        row = max(row, 0 + BORDER)
        column = min(column + columns_direction, max_column - BORDER)
        column = max(column, 0 + BORDER)
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
def draw_frame(canvas, start_row, start_column, text, negative=False):
    """Draw multiline text fragment on canvas, erase text instead of drawing if negative=True is specified."""

    rows_number, columns_number = canvas.getmaxyx()

    for row, line in enumerate(text.splitlines(), round(start_row)):
        if row < 0:
            continue

        if row >= rows_number:
            break

        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue

            if column >= columns_number:
                break

            if symbol == ' ':
                continue

            # Check that current position it is not in a lower right corner of the window
            # Curses will raise exception in that case. Don`t ask why…
            # https://docs.python.org/3/library/curses.html#curses.window.addch
            if row == rows_number - 1 and column == columns_number - 1:
                continue

            symbol = symbol if not negative else ' '
            canvas.addch(row, column, symbol)

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

