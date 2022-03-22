"""Module with utilities for game running."""

from collections.abc import Iterator
from itertools import cycle

SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258


def read_controls(canvas) -> tuple:
    """Read keys pressed and return tuple witl controls state.

    Args:
        canvas: playing field.
    """
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


def get_frame_size(text) -> tuple:
    """Calculate size of multiline text fragment.

    Args:
        text: object to be parsed.

    Returns:
        Size pair (rows number, colums number).
    """
    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])
    return rows, columns


def draw_frame(canvas, start_row, start_column, text, negative=False):
    """Draw multiline text fragment on canvas.

    Args:
        canvas: playing field.
        start_row: initianl position of drawing (Y).
        start_column: initial position of drwaing (X).
        text: multiline fragment to be drawn.
        negative: erase text instead of drawing if negative=True is specified.
    """
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


def cycle_object_frames(paths_to_frames)->Iterator[str]:
    """Create iterator of object frames for animation.

    Args:
        paths_to_frames: paths to files with frames.

    Returns:
        Cycle iterator with object frames.
    """
    frames = []
    for path in paths_to_frames:
        with open(path) as frame_file:
            frame = frame_file.read()
        frames.append(frame)
    return cycle(frames)
