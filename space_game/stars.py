"""Module for stars objects."""

import asyncio
import curses
import random

from settings import (
    BORDER_THICKNESS, BRIGHT_LIFETIME, COMMON_LIFETIME, DIM_LIFETIME, STAR_APPEARANCE_TIMEOUT,
    STAR_QUANTITY, STAR_SYMBOLS,
)


async def blink(canvas, row, column, symbol):
    """Create star with lifecycle as a coroutine.

    Args:
        canvas: playing field.
        row: poisition of a star (Y).
        column: position of a star (X).
        symbol: form of a star.
    """
    canvas.addstr(row, column, symbol, curses.A_DIM)
    for _ in range(random.randint(1, STAR_APPEARANCE_TIMEOUT)):
        await asyncio.sleep(0)

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(DIM_LIFETIME):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(COMMON_LIFETIME):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(BRIGHT_LIFETIME):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(COMMON_LIFETIME):
            await asyncio.sleep(0)


def get_stars(canvas) -> list:
    """Create many stars all over the playing field.

    Args:
        canvas: playing field.

    Returns:
        List of stars (coroutines).
    """
    max_row, max_column = canvas.getmaxyx()
    return [
        blink(
            canvas,
            row=random.randint(1, max_row - BORDER_THICKNESS),
            column=random.randint(1, max_column - BORDER_THICKNESS),
            symbol=random.choice(STAR_SYMBOLS),
        ) for _ in range(STAR_QUANTITY)
    ]
