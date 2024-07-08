from common import *

import numpy as np
from typing import *

# concepts:
# topology

# description:
# The input grid is a square grid with black and green pixels. The input grid should have regions that are enclosed by the green pixels. 
# To produce the output, you need to find the enclosed regions in the input grid, and then color them yellow. 
                
def main(input_grid):
    # Create initial output grid template based on input grid.
    output_grid = input_grid.copy()

    # Find enclosed regions
    interior_mask = object_interior(input_grid)
    boundary_mask = object_boundary(input_grid)
    inside_but_not_on_edge = interior_mask & ~boundary_mask

    # Color enclosed regions
    for x, y in np.argwhere(inside_but_not_on_edge):
        if output_grid[x, y] == Color.BLACK:
            output_grid[x, y] = Color.YELLOW

    return output_grid


def generate_input():
    # Generate a square grid of arbitrary size with black background, size from 5x5 to 20x20
    n = random.randint(10, 20)
    grid = np.zeros((n, n), dtype=int)

    # Generate some random green sprites, and then hollow out the interior
    n_objects = random.randint(1, 3)
    for _ in range(n_objects):
        n, m = random.randint(4, 10), random.randint(4, 10)
        sprite = random_sprite(n, m, color_palette=[Color.GREEN], connectivity=8)
        interior_mask = object_interior(sprite)
        boundary_mask = object_boundary(sprite)
        interior_but_not_edges = interior_mask & ~boundary_mask
        sprite[interior_but_not_edges] = Color.BLACK

        try:
            x, y = random_free_location_for_sprite(grid, sprite, border_size=1, padding=1)
        except:
            continue

        blit_sprite(grid, sprite, x, y, background=Color.BLACK)
    
    return grid 

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
