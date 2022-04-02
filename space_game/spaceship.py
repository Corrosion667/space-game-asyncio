"""Module for spaceship object and its gunfire."""

import asyncio
import curses

from space_game.settings import BORDER_THICKNESS, FIRE_COLUMNS_SPEED, FIRE_ROWS_SPEED
from space_game.utils import draw_frame, get_frame_size, read_controls


async def fire(
    canvas, start_row, start_column, rows_speed=FIRE_ROWS_SPEED, columns_speed=FIRE_COLUMNS_SPEED,
):
    """Display animation of gun shot, direction and speed can be specified.

    Args:
        canvas: playing field.
        start_row: initial position of fire object (Y).
        start_column: initial position of fire object (X).
        rows_speed: movement within rows through time,
        columns_speed: movement within columns through time
    """
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


async def animate_spaceship(canvas, row, column, ship_frames):
    """Display animation of spaceship, which can be controlled with arrows.

    Args:
        canvas: playing field.
        row: position where to display spaceship (Y).
        column: position where to display spaceship (X).
        ship_frames: frames put in a cycle.
    """
    for spaceship in ship_frames:
        max_row, max_column = canvas.getmaxyx()
        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        frame_rows, frame_columns = get_frame_size(spaceship)
        row = min(row + rows_direction, max_row - frame_rows - BORDER_THICKNESS)
        row = max(row, BORDER_THICKNESS)
        column = min(column + columns_direction, max_column - frame_columns - BORDER_THICKNESS)
        column = max(column, BORDER_THICKNESS)
        draw_frame(canvas, row, column, spaceship, negative=False)
        for _ in range(2):
            await asyncio.sleep(0)
        draw_frame(canvas, row, column, spaceship, negative=True)
