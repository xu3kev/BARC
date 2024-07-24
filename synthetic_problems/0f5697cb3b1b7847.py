from common import *

import numpy as np
from typing import *

# concepts:
# topology, symmetry detection

# description:
# The input grid is a square grid with black and green pixels, forming enclosed regions with vertical symmetry within the green areas.
# To produce the output, you need to find the enclosed regions and color them based on their symmetry.
# Color the region blue if symmetric, otherwise color the region yellow.

def main(input_grid):
    output_grid = input_grid.copy()

    # Find enclosed regions
    interior_mask = object_interior(input_grid)
    boundary_mask = object_boundary(input_grid)
    inside_but_not_on_edge = interior_mask & ~boundary_mask

    for x, y in np.argwhere(inside_but_not_on_edge):
        # Extract the region
        region = input_grid[x-1:x+2, y-1:y+2]

        # Check for vertical symmetry in the region
        if np.all(region == np.flip(region, axis=1)):
            output_grid[x, y] = Color.BLUE
        else:
            output_grid[x, y] = Color.YELLOW

    return output_grid


def generate_input():
    # Generate a square grid of arbitrary size with black background, size from 10x10 to 20x20
    n = random.randint(10, 20)
    grid = np.zeros((n, n), dtype=int)

    # Generate some random green sprites, ensuring vertical symmetry
    n_objects = random.randint(1, 3)
    for _ in range(n_objects):
        n, m = random.randint(4, 8), random.randint(4, 8)

        # Generate a symmetric sprite
        sprite = random_sprite(n, m//2, color_palette=[Color.GREEN], connectivity=8)
        sprite = np.concatenate([sprite, np.flip(sprite, axis=1)], axis=1)

        # Hollow out the interior areas of the sprite
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