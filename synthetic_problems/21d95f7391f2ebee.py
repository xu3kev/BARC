from common import *

import numpy as np
from typing import *

# concepts:
# patterns, repetition, color guide, objects

# description:
# In the input grid, you will have objects of varying shapes and colors on a black background.
# The grid will also have a vertical colored bar on either the left or right side of the grid, representing a "color guide".
# To produce the output, replicate each row of the grid horizontally to the right, as many times as the color of the object matches the index in the color guide (1-based index).

def main(input_grid):
    # Find the color guide
    color_guide_col = 0 if any(input_grid[:, 0] != Color.BLACK) else -1
    color_guide = [input_grid[i, color_guide_col] for i in range(input_grid.shape[0]) if input_grid[i, color_guide_col] != Color.BLACK]

    # Prepare the output grid
    max_reps = len(color_guide)
    output_grid = np.zeros((input_grid.shape[0], input_grid.shape[1] * max_reps), dtype=int)

    # Replicate rows according to the color guide
    for row in range(input_grid.shape[0]):
        for col in range(input_grid.shape[1]):
            color = input_grid[row, col]
            if color != Color.BLACK:
                if color in color_guide:
                    reps = color_guide.index(color) + 1
                    for rep in range(reps):
                        output_grid[row, col + rep * input_grid.shape[1]] = color

    return output_grid

def generate_input():
    # Create a black 10x10 grid as the background
    n = m = 10
    grid = np.zeros((n, m), dtype=int)
    
    # Generate the color guide
    color_guide_col = 0 if np.random.rand() > 0.5 else -1
    unique_colors = list(Color.NOT_BLACK)
    np.random.shuffle(unique_colors)
    guide_length = np.random.randint(1, 6)
    for i in range(guide_length):
        grid[i, color_guide_col] = unique_colors[i]

    # Generate random objects on the grid
    num_objects = np.random.randint(3, 7)
    for _ in range(num_objects):
        sprite = random_sprite(np.random.randint(1, 4), np.random.randint(1, 4), symmetry="not_symmetric", color_palette=[np.random.choice(unique_colors)])
        try:
            x, y = random_free_location_for_sprite(grid, sprite, padding=1, padding_connectivity=8)
            blit_sprite(grid, sprite, x=x, y=y)
        except:
            pass

    return grid