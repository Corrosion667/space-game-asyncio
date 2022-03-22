"""Module with constants affecting the game."""

# general
TIC_TIMEOUT = 0.1
BORDER_THICKNESS = 1

# stars
STAR_QUANTITY = 250
STAR_SYMBOLS = ('+', '*', '.', ':')
STAR_APPEARANCE_TIMEOUT = 100
DIM_LIFETIME = 20
BRIGHT_LIFETIME = 5
COMMON_LIFETIME = 3

# fire
FIRE_ROWS_SPEED = -0.3
FIRE_COLUMNS_SPEED = -0.3

# spaceship
SPACESHIP_FRAMES = (
    '/space_game/frames/rocket/rocket_frame_1.txt',
    '/space_game/frames/rocket/rocket_frame_2.txt',
)
INITIAL_SPACESHIP_POSITION_SHIFT = 2
