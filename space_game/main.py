import curses
import asyncio
import time
import random

TIC_TIMEOUT = 0.1
BORDER = 1

STAR_SYMBOLS = ('+', '*', '.', ':')


async def blink(canvas, row, column, symbol='*'):
    canvas.addstr(row, column, symbol, curses.A_DIM)
    for _ in range(random.randint(1, 100)):
        await asyncio.sleep(0)
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(20):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)


def get_stars(canvas):
    star_quantity = 200
    max_y, max_x = canvas.getmaxyx()
    stars = [
        blink(
            canvas,
            row=random.randint(1, max_y - BORDER),
            column=random.randint(1, max_x - BORDER),
            symbol=random.choice(STAR_SYMBOLS),
        ) for _ in range(star_quantity)
    ]
    return stars


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
    stars = get_stars(canvas)
    max_y, max_x = canvas.getmaxyx()
    fire_start_row = max_y // 2
    fire_start_colunm = max_x // 2
    courutines = [*stars, fire(canvas, fire_start_row, fire_start_colunm)]
    while True:
        for courutine in courutines.copy():
            try:
                courutine.send(None)
            except StopIteration:
                courutines.remove(courutine)
        canvas.border()
        canvas.refresh()
        time.sleep(0.1)



if __name__ == '__main__':
    curses.initscr()
    curses.update_lines_cols()
    curses.curs_set(0)
    curses.wrapper(draw)

