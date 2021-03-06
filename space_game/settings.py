"""Module with constants affecting the game."""

import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# general
TIC_TIMEOUT = 0.1
BORDER_THICKNESS = 1

# stars
STAR_QUANTITY = 250
STAR_SYMBOLS = ('+', '*', '.', ':')
MAX_STAR_APPEARANCE_TIMEOUT = 100
DIM_LIFETIME = 20
BRIGHT_LIFETIME = 5
COMMON_LIFETIME = 3

# fire
FIRE_ROWS_SPEED = -0.3
FIRE_COLUMNS_SPEED = 0

# spaceship
SPACESHIP_FRAMES_PATHS = (
    os.path.join(BASE_DIR, 'frames/rocket/rocket_frame_1.txt'),
    os.path.join(BASE_DIR, 'frames/rocket/rocket_frame_2.txt'),
)
INITIAL_SPACESHIP_POSITION_SHIFT = 2

# garbage
GARBAGE_TYPES_PATHS = (
    os.path.join(BASE_DIR, 'frames/space_garbage/duck.txt'),
    os.path.join(BASE_DIR, 'frames/space_garbage/hubble.txt'),
    os.path.join(BASE_DIR, 'frames/space_garbage/lamp.txt'),
    os.path.join(BASE_DIR, 'frames/space_garbage/trash_large.txt'),
    os.path.join(BASE_DIR, 'frames/space_garbage/trash_small.txt'),
    os.path.join(BASE_DIR, 'frames/space_garbage/trash_xl.txt'),
)
GARBAGE_SPEED = 0.5
