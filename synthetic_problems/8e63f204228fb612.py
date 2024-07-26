from common import *

import numpy as np
from typing import *

# concepts:
# patterns, topology, color

# description:
# The input grid is filled with random colored shapes on a black background. Some shapes may have
# enclosed regions creating holes. Identify the enclosed regions and fill them with colors in
# a sequence order of Blue, Red, Green, and repeat.

def main(input_grid):
    # Create initial output grid template based on input grid.
    output_grid = input_grid.copy()

    # Find enclosed regions
    interior_mask = object_interior(input_grid)
    boundary_mask = object_boundary(input_grid)
    inside_but_not_on_edge = interior_mask & ~boundary_mask

    # Define the color sequence
    colors = [Color.BLUE, Color.RED, Color.GREEN]
    color_index = 0
    
    # Color enclosed regions
    for x, y in np.argwhere(inside_but_not_on_edge):
        if output_grid[x, y] == Color.BLACK:
            output_grid[x, y] = colors[color_index]
            color_index = (color_index + 1) % len(colors)

    return output_grid

def generate_input():
    # Generate a grid of arbitrary size with black background, size from 10x10 to 20x20
    n = random.randint(10, 20)
    grid = np.zeros((n, n), dtype=int)

    # Generate random colored shapes and hollow out the interior to create enclosed regions
    n_objects = random.randint(2, 5)
    for _ in range(n_objects):
        n, m = random.randint(4, 8), random.randint(4, 8)
        color_palette = list(random.sample(set(Color.ALL_COLORS) - {Color.BLACK}, random.randint(1, 3)))
        sprite = random_sprite(n, m, color_palette=color_palette, connectivity=8)
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