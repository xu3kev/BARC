from common import *

import numpy as np
from typing import *

# concepts:
# translational symmetry, repetition, Coloring diagonal pixels

# description:
# Given an input grid, replicate the input grid on a larger canvas multiple times.
# If any two identical colored pixels share the same coordinate on different grid repetitions,
# color all diagonally adjacent pixels teal if they are black, producing a specific patterned output.

def main(input_grid):
    # Determine size of input grid
    input_height, input_width = input_grid.shape

    # Calculate the number of repetitions for the larger canvas
    repetitions_x = 4  # number of times to replicate input along x direction
    repetitions_y = 4  # number of times to replicate input along y direction

    # Initialize larger output grid
    output_height, output_width = input_height * repetitions_x, input_width * repetitions_y
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Blit the input grid multiple times on the larger canvas
    for i in range(repetitions_x):
        for j in range(repetitions_y):
            blit_sprite(output_grid, input_grid, x=i * input_height, y=j * input_width)

    # Create diagonal directions
    diagonal_directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

    # Color diagonally adjacent pixels teal if they are black
    for y in range(output_width):
        for x in range(output_height):
            if output_grid[x, y] != Color.BLACK and output_grid[x, y] != Color.TEAL:
                for dx, dy in diagonal_directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < output_height and 0 <= ny < output_width and output_grid[nx, ny] == Color.BLACK:
                        output_grid[nx, ny] = Color.TEAL

    return output_grid

def generate_input():
    # Define grid size for input
    n, m = np.random.randint(3, 8), np.random.randint(3, 8)

    # Initialize input grid with black background
    grid = np.zeros((n, m), dtype=int)

    # Select number of colored pixels
    n_colored_pixels = np.random.randint(1, min(n, m))

    # Select random color from predefined set (excluding teal and black)
    pixel_color = np.random.choice(list(Color.NOT_BLACK))
    while pixel_color == Color.TEAL:
        pixel_color = np.random.choice(list(Color.NOT_BLACK))

    # Add colored pixels to random locations in the grid
    sprite = np.array([[pixel_color]])
    for _ in range(n_colored_pixels):
        x, y = random_free_location_for_sprite(grid, sprite)
        blit_sprite(grid, sprite, x, y)

    return grid