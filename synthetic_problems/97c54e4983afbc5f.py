from common import *

import numpy as np
from typing import *

# concepts:
# patterns, colors, symmetry detection

# description:
# In the input, you will see a grid containing various shapes of different colors. 
# To make the output, detect the reflected symmetrical counterparts of all shapes along the vertical axis of the grid. 
# If a mirrored symmetrical shape is missing, fill in those pixels with the same color to complete the symmetry.

def main(input_grid):
    output_grid = np.copy(input_grid)

    # Find the center vertical axis of reflection
    center_axis = input_grid.shape[1] // 2

    # Iterate through the grid to check for symmetrical counterparts
    for x in range(input_grid.shape[0]):
        for y in range(center_axis + 1):
            color = input_grid[x, y]
            if color != Color.BLACK:
                mirrored_y = 2 * center_axis - y
                if mirrored_y < input_grid.shape[1] and input_grid[x, mirrored_y] == Color.BLACK:
                    output_grid[x, mirrored_y] = color

    return output_grid


def generate_input():
    # dimensions of the grid
    n = np.random.randint(6, 10)
    m = 2 * np.random.randint(5, 8)
    
    # create a black grid
    grid = np.full((n, m), Color.BLACK, dtype=int)
    
    # add symmetric shapes with colors
    num_shapes = np.random.randint(2, 5)
    for _ in range(num_shapes):
        color = np.random.choice(list(Color.NOT_BLACK))
        shape_width = np.random.randint(2, m // 2)
        shape_height = np.random.randint(2, n)
        
        # Create a random shape
        shape = random_sprite(shape_height, shape_width, color_palette=[color], background=Color.BLACK)
        
        # Randomly place the left half of the shape
        x = np.random.randint(0, n - shape_height)
        y = np.random.randint(0, m // 2 - shape_width)
        
        # Place the shape and its symmetric counterpart
        blit_sprite(grid, shape, x, y)
        mirrored_shape = np.fliplr(shape)
        blit_sprite(grid, mirrored_shape, x, 2 * (m // 2) - y - shape_width)
        
        # Randomly remove part of the mirrored shape for the puzzle challenge
        remove_height = np.random.randint(0, shape_height)
        remove_width = np.random.randint(0, shape_width)
        grid[x:x+remove_height, 2 * (m // 2) - y - shape_width: 2 * (m // 2) - y - shape_width + remove_width] = Color.BLACK

    return grid