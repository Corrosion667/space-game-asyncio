"""Module for space garbage objects."""

import asyncio

from space_game.canvas_tools import draw_frame
from space_game.settings import BORDER_THICKNESS, GARBAGE_SPEED


async def fly_garbage(canvas, column, garbage_frame, speed=GARBAGE_SPEED):
    """Animate garbage, flying from top to bottom.

    Column position will stay same, as specified on start.

    Args:
        canvas: playing field.
        column: initial position of a garbage object (X).
        garbage_frame: form of a garbage object.
        speed: how many rows garbage object flies within one game tic.
    """
    max_row, max_column = canvas.getmaxyx()
    column = max(column, 0)
    column = min(column, max_column - BORDER_THICKNESS)
    row = 0
    while row < max_row:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed
