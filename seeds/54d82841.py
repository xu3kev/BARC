from common import *

import numpy as np
from typing import *

# concepts:
# gravity, falling

# description:
# In the input you will see various monochromatic objects
# To make the output, make each object drop a single yellow pixel below it, centered with the middle of the object

def main(input_grid):
    # Plan:
    # 1. Detect the objects
    # 2. Drop yellow pixels which land in the final row of the grid, centered with the middle of the object

    objects = find_connected_components(input_grid, connectivity=4, background=Color.BLACK, monochromatic=True)

    output_grid = input_grid.copy()

    for obj in objects:
        x, y = object_position(obj, background=Color.BLACK, anchor='center')
        bottom_y = output_grid.shape[1] - 1
        output_grid[x, bottom_y] = Color.YELLOW
    
    return output_grid


def generate_input():
    width, height = np.random.randint(10, 30), np.random.randint(10, 30)
    grid = np.full((width, height), Color.BLACK)
    
    n_objects = np.random.randint(1, 5)
    for _ in range(n_objects):
        # Make a random sprite with odd width, so that there will be a unique horizontally center pixel 
        widths = [3, 5, 7]
        heights = [1,2,3,4]
        sprite = random_sprite(widths, heights, color_palette=[random.choice(Color.NOT_BLACK)])
        # Find a place for it, but put some padding along the borders so that it's not at the bottom
        x, y = random_free_location_for_sprite(grid, sprite, padding=2, border_size=2)
        # Put it down
        blit_sprite(grid, sprite, x, y)

    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
