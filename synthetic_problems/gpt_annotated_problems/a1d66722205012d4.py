from common import *

import numpy as np
from typing import *

# concepts:
# topology, connectivity, symmetry detection

# description:
# The input grid contains black, green, and blue pixels. The green pixels form enclosed regions, and the blue pixels form a single connected component.
# To produce the output:
# 1. Find all enclosed regions formed by green pixels and fill them with yellow.
# 2. If the blue component is symmetric (either horizontally or vertically), color it red.
# 3. If the blue component touches (is adjacent to) any yellow region, color that yellow region orange.

def main(input_grid):
    output_grid = input_grid.copy()

    # Step 1: Fill enclosed regions with yellow
    interior_mask = object_interior(input_grid, background=Color.BLACK)
    boundary_mask = object_boundary(input_grid, background=Color.BLACK)
    inside_but_not_on_edge = interior_mask & ~boundary_mask
    
    for x, y in np.argwhere(inside_but_not_on_edge):
        if output_grid[x, y] == Color.BLACK:
            output_grid[x, y] = Color.YELLOW

    # Step 2: Check if blue component is symmetric and color it red if so
    blue_mask = input_grid == Color.BLUE
    blue_component = np.zeros_like(input_grid)
    blue_component[blue_mask] = Color.BLUE
    
    horizontally_symmetric = np.array_equal(blue_component, np.flip(blue_component, axis=1))
    vertically_symmetric = np.array_equal(blue_component, np.flip(blue_component, axis=0))
    
    if horizontally_symmetric or vertically_symmetric:
        output_grid[blue_mask] = Color.RED

    # Step 3: Color yellow regions orange if they touch blue
    yellow_regions = find_connected_components(output_grid, background=Color.BLACK)
    blue_or_red = (output_grid == Color.BLUE) | (output_grid == Color.RED)
    
    for region in yellow_regions:
        if np.any(region == Color.YELLOW):
            touches_blue = contact(object1=region, object2=blue_or_red)
            if touches_blue:
                output_grid[region == Color.YELLOW] = Color.ORANGE

    return output_grid

def generate_input():
    # Generate a square grid of arbitrary size with black background
    n = random.randint(15, 25)
    grid = np.zeros((n, n), dtype=int)

    # Generate some random green enclosures
    n_enclosures = random.randint(2, 4)
    for _ in range(n_enclosures):
        size = random.randint(4, 8)
        sprite = random_sprite(size, size, color_palette=[Color.GREEN], connectivity=8)
        interior_mask = object_interior(sprite)
        boundary_mask = object_boundary(sprite)
        interior_but_not_edges = interior_mask & ~boundary_mask
        sprite[interior_but_not_edges] = Color.BLACK

        try:
            x, y = random_free_location_for_sprite(grid, sprite, border_size=1, padding=1)
            blit_sprite(grid, sprite, x, y, background=Color.BLACK)
        except:
            continue

    # Generate a blue component (possibly symmetric)
    blue_size = random.randint(5, 10)
    blue_sprite = random_sprite(blue_size, blue_size, color_palette=[Color.BLUE], density=0.7)
    
    if random.choice([True, False]):  # 50% chance of being symmetric
        symmetry = random.choice(['horizontal', 'vertical'])
        if symmetry == 'horizontal':
            blue_sprite = np.concatenate((blue_sprite, np.flip(blue_sprite, axis=1)), axis=1)
        else:
            blue_sprite = np.concatenate((blue_sprite, np.flip(blue_sprite, axis=0)), axis=0)

    try:
        x, y = random_free_location_for_sprite(grid, blue_sprite, border_size=1, padding=1)
        blit_sprite(grid, blue_sprite, x, y, background=Color.BLACK)
    except:
        pass  # If we can't place the blue sprite, just continue without it

    return grid