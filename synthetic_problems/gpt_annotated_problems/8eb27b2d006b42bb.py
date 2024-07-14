from common import *

import numpy as np
from typing import *

# concepts:
# symmetry detection, growing, occlusion

# description:
# In the input, you will see a partially occluded rotationally symmetric object.
# To make the output, first fill in the missing parts to complete the rotational symmetry.
# Then, grow the object outward by one pixel in all directions, maintaining the rotational symmetry.

def main(input_grid):
    output_grid = input_grid.copy()
    
    # Step 1: Complete the rotational symmetry
    sym = detect_rotational_symmetry(input_grid, ignore_colors=[Color.BLACK])
    colored_pixels = np.argwhere(input_grid != Color.BLACK)
    
    for x, y in colored_pixels:
        color = input_grid[x, y]
        for i in range(1, 4):
            rotated_x, rotated_y = sym.apply(x, y, iters=i)
            if output_grid[rotated_x, rotated_y] == Color.BLACK:
                output_grid[rotated_x, rotated_y] = color
    
    # Step 2: Grow the object
    growth_grid = np.zeros_like(output_grid)
    
    for x in range(output_grid.shape[0]):
        for y in range(output_grid.shape[1]):
            if output_grid[x, y] != Color.BLACK:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < output_grid.shape[0] and 0 <= ny < output_grid.shape[1]:
                            growth_grid[nx, ny] = output_grid[x, y]
    
    # Ensure rotational symmetry in the grown object
    for x in range(growth_grid.shape[0]):
        for y in range(growth_grid.shape[1]):
            if growth_grid[x, y] != Color.BLACK:
                color = growth_grid[x, y]
                for i in range(1, 4):
                    rotated_x, rotated_y = sym.apply(x, y, iters=i)
                    if 0 <= rotated_x < growth_grid.shape[0] and 0 <= rotated_y < growth_grid.shape[1]:
                        growth_grid[rotated_x, rotated_y] = color
    
    return growth_grid

def generate_input():
    # Initialize 12x12 grid
    grid = np.zeros((12, 12), dtype=int)

    # Create 7x7 sprite
    sprite = random_sprite(
        7, 7, density=0.4, symmetry="radial", color_palette=list(Color.NOT_BLACK)
    )

    # Randomly remove pixels from sprite
    for i in range(sprite.shape[0]):
        for j in range(sprite.shape[1]):
            if random.random() < 0.3:
                sprite[i, j] = Color.BLACK

    # Place sprite at the center of the grid
    x, y = 2, 2
    blit_sprite(grid, sprite, x, y)

    return grid