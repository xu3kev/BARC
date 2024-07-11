from common import *

import numpy as np
from typing import *

# concepts:
# surrounding, objects

# description:
# In the input, you will see several colored objects of various shapes.
# To make the output, surround each object with a one-pixel border of its own color.
# The border should not overlap with other objects or their borders.
# If two objects of the same color are adjacent, their borders should merge.

def main(input_grid):
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Function to get the color of an object at a given position
    def get_object_color(x, y):
        return input_grid[x, y] if input_grid[x, y] != Color.BLACK else None

    # Function to add border around a pixel if it's part of an object
    def add_border(x, y, color):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < height and 0 <= ny < width:
                    if output_grid[nx, ny] == Color.BLACK:
                        output_grid[nx, ny] = color

    # Iterate through the grid
    for x in range(height):
        for y in range(width):
            color = get_object_color(x, y)
            if color:
                add_border(x, y, color)

    return output_grid

def generate_input():
    grid = np.zeros((15, 15), dtype=int)
    
    # Generate 3-5 random objects
    num_objects = np.random.randint(3, 6)
    for _ in range(num_objects):
        color = np.random.choice(list(Color.NOT_BLACK))
        sprite = random_sprite(
            n=np.random.randint(2, 5),
            m=np.random.randint(2, 5),
            density=0.7,
            symmetry="not_symmetric",
            color_palette=[color]
        )
        x, y = random_free_location_for_sprite(grid, sprite, padding=1)
        blit_sprite(grid, sprite, x, y)
    
    return grid