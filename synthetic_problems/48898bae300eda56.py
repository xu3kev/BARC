from common import *

import numpy as np
from typing import *

# concepts:
# shapes, counting, symmetry

# description:
# In the input, you will see arbitrarily shaped, multicolored objects on a black background.
# To make the output, count the number of distinct colors in each object and then color the entire object with one color based on the count:
# - If the object contains exactly one color, color it maroon.
# - If the object contains exactly two colors, color it orange.
# - If the object contains three or more colors, color it teal.

def main(input_grid):
    output_grid = np.copy(input_grid)
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=8, monochromatic=False)

    for obj in objects:
        unique_colors = set(np.unique(obj))
        unique_colors.discard(Color.BLACK)

        color_count = len(unique_colors)
        
        if color_count == 1:
            new_color = Color.MAROON
        elif color_count == 2:
            new_color = Color.ORANGE
        else:
            new_color = Color.TEAL

        output_grid[obj != Color.BLACK] = new_color

    return output_grid

def generate_input():
    n, m = 12, 12
    grid = np.full((n, m), Color.BLACK, dtype=int)

    num_shapes = np.random.randint(3, 7)
    for _ in range(num_shapes):
        width = np.random.randint(2, 5)
        height = np.random.randint(2, 5)
        sprite = random_sprite(width, height, color_palette=random.sample(Color.NOT_BLACK, np.random.randint(1, 4)), connectivity=8)

        try:
            x, y = random_free_location_for_sprite(grid, sprite)
            blit_sprite(grid, sprite, x, y)
        except:
            continue

    return grid