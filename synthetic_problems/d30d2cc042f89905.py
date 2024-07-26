from common import *
import numpy as np
from typing import *

# concepts:
# Coloring adjacent pixels, repetition

# description:
# Given an input grid of arbitrary size, with some small number of colored pixels on it.
# To produce the output, replicate the input grid 4 times, 2 on the top and 2 on the bottom.
# Color all the adjacent pixels (up, down, left, right) orange if they are black and adjacent to a green pixel.

def main(input_grid):
    # Replicate input grid 4 times to initialize output grid
    output_grid = np.zeros((2 * input_grid.shape[0], 2 * input_grid.shape[1]), dtype=int)
    for i in range(2):
        for j in range(2):
            blit_sprite(output_grid, input_grid, i * input_grid.shape[0], j * input_grid.shape[1])

    # Create adjacent directions
    adjacent_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # Color adjacent pixels orange if they are black and adjacent to a green pixel
    for y in range(output_grid.shape[1]):
        for x in range(output_grid.shape[0]):
            if output_grid[x, y] == Color.GREEN:
                for dx, dy in adjacent_directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < output_grid.shape[0] and 0 <= ny < output_grid.shape[1] and output_grid[nx, ny] == Color.BLACK:
                        output_grid[nx, ny] = Color.ORANGE
    
    return output_grid

def generate_input():
    # Random size of input grid
    n, m = np.random.randint(2, 6), np.random.randint(2, 6)

    # Initialize grid
    grid = np.zeros((n, m), dtype=int)

    # Have 1 to 4 number of green colored pixels in the initial square
    n_colored_pixels = np.random.randint(1, 5)

    # Create a dummy sprite with one green pixel.
    sprite = np.array([Color.GREEN]).reshape(1, 1)

    # Randomly place n_colored_pixels in the grid
    for _ in range(n_colored_pixels):
        x, y = random_free_location_for_sprite(grid, sprite)
        blit_sprite(grid, sprite, x, y)

    return grid