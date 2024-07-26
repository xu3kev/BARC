from common import *

import numpy as np
from typing import *

# concepts:
# objects, color, falling

# description:
# In the input grid, you will see colored objects scattered around a black background. At the bottom of the grid, there is a horizontal line of gray pixels. 
# To make the output, make the colored objects fall to the bottom and rest on top of the gray line. The goal is to make all objects fall naturally.

def main(input_grid):
    output_grid = np.copy(input_grid)

    width, height = output_grid.shape

    # Find the color of the bottom line
    bottom_line_color = Color.GRAY

    # Find the color of the background, which is the most common color
    background_color = np.argmax(np.bincount(output_grid.flatten()))

    # Process each column to perform the falling operation
    for x in range(width):
        for y in range(height-2, -1, -1):
            if output_grid[x, y] != background_color:
                # Find the lowest position where this object can fall
                for k in range(y, height-1):
                    if output_grid[x, k+1] in (background_color, bottom_line_color):
                        output_grid[x, k+1] = output_grid[x, k]
                        output_grid[x, k] = background_color
                    else:
                        break

    return output_grid


def generate_input():
    # Initialize the input grid with black pixels
    width, height = 10, 10
    input_grid = np.zeros((width, height), dtype=int)

    # Choose a few colors for objects
    colors = np.random.choice(list(Color.NOT_BLACK), size=3, replace=False)

    # Randomly place the objects in the grid
    for _ in range(5):
        object_color = np.random.choice(colors)
        x, y = np.random.randint(0, width), np.random.randint(0, height - 1)
        input_grid[x, y] = object_color

    # Create a gray line at the bottom row
    input_grid[:, height-1] = Color.GRAY

    return input_grid