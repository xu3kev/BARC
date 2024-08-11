from common import *

import numpy as np
import random
from typing import *

# concepts:
# Coloring diagonal pixels, repetition, symmetry

# description:
# Given an input grid of arbitrary size containing a small number (1-4) of colored pixels.
# To produce the output, replicate the input grid 2 times; copy the grid once and reflect it horizontally to place them side by side.
# Color all the diagonal and orthogonal pixels adjacent to a colored pixel with pink and orange respectively if they are originally black.

def main(input_grid):
    # Reflect input grid horizontally and create output grid by placing original and the reflection side by side
    reflected_grid = np.copy(np.fliplr(input_grid))
    output_grid = np.concatenate((input_grid, reflected_grid), axis=1)
    
    # Directions for coloring pixels
    diagonal_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    orthogonal_directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    # Loop through cells and color adjacent pixels
    for y in range(output_grid.shape[1]):
        for x in range(output_grid.shape[0]):
            if output_grid[x, y] != Color.BLACK and output_grid[x, y] != Color.PINK and output_grid[x, y] != Color.ORANGE:
                for dx, dy in diagonal_directions:
                    if 0 <= x + dx < output_grid.shape[0] and 0 <= y + dy < output_grid.shape[1] and output_grid[x + dx, y + dy] == Color.BLACK:
                        output_grid[x + dx, y + dy] = Color.PINK
                for dx, dy in orthogonal_directions:
                    if 0 <= x + dx < output_grid.shape[0] and 0 <= y + dy < output_grid.shape[1] and output_grid[x + dx, y + dy] == Color.BLACK:
                        output_grid[x + dx, y + dy] = Color.ORANGE
    
    return output_grid


def generate_input():
    # Have 1 to 4 number of colored pixels in the initial square
    n_colored_pixels = random.randint(1, 4)
    
    # Random pixel color that is not black, pink, or orange
    pixel_color = random.choice(list(Color.NOT_BLACK))
    while pixel_color in [Color.PINK, Color.ORANGE]:
        pixel_color = random.choice(list(Color.NOT_BLACK))

    # Random size of input grid
    n, m = random.randint(2, 10), random.randint(2, 10)

    # Initialize grid
    grid = np.zeros((n, m), dtype=int)
  
    # Create a dummy sprite with one pixel
    sprite = np.array([pixel_color]).reshape(1, 1)
    
    # Randomly place n_colored_pixels pixels on the grid
    for _ in range(n_colored_pixels):
        x, y = random_free_location_for_sprite(grid, sprite)
        blit_sprite(grid, sprite, x, y)

    return grid