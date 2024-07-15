from common import *

import numpy as np
from typing import *

# concepts:
# Coloring diagonal pixels, repetition, objects

# description:
# Given an input grid of arbitrary size, with some small number of colored squares (objects) on it.
# To produce the output, replicate the grid 3 times vertically.
# Each replication adds a border around existing objects by coloring all the adjacent black pixels (north, south, east, and west) with the same color.
# The first replication does nothing other than copying the input grid.
# The second replication adds a border around the original colored squares in the input.
# The third replication adds an additional border around the squares obtained in the second replication.

def main(input_grid):
    height, width = input_grid.shape
    output_grid = np.zeros((3 * height, width), dtype=int)

    # Function to add border around objects
    def add_border(grid, start_x, start_y):
        expanded_grid = grid.copy()
        for x in range(height):
            for y in range(width):
                if grid[x, y] != Color.BLACK:
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < height and 0 <= ny < width and expanded_grid[nx, ny] == Color.BLACK:
                            expanded_grid[nx, ny] = grid[x, y]
        return expanded_grid

    # First copy is identical to the input grid
    output_grid[:height, :width] = input_grid

    # Second replication adds a border around original colored squares
    bordered_grid = add_border(input_grid, 0, 0)
    output_grid[height:2*height, :width] = bordered_grid

    # Third replication adds further border around the new squares
    double_bordered_grid = add_border(bordered_grid, height, 0)
    output_grid[2*height:3*height, :width] = double_bordered_grid
    
    return output_grid

def generate_input():
    # Have 1 to 4 number of colored squares (objects) in the initial grid
    n_colored_squares = random.randint(1, 4)
    
    # Random color that is not black
    object_color = random.choice(list(Color.NOT_BLACK))

    # Random size of the input grid
    n, m = random.randint(3, 8), random.randint(3, 8)

    # Initialize grid
    grid = np.zeros((n, m), dtype=int)
    
    # Create a 2x2 colored square (object)
    sprite = np.full((2, 2), object_color)
    
    # Randomly place n_colored_squares objects on the grid
    for _ in range(n_colored_squares):
        x, y = random_free_location_for_sprite(grid, sprite)
        blit_sprite(grid, sprite, x, y)

    return grid