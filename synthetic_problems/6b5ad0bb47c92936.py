from common import *

import numpy as np
from typing import *

# concepts:
# reflection, symmetry detection, scaling

# description:
# In the input, you will see a symmetric sprite placed on a grid. Some parts may be missing (occluded by black).
# To make the output: 
# 1. Detect the symmetry of the sprite.
# 2. Scale up the sprite by replacing each pixel with a 2x2 block of the same color.
# 3. Ensure that the scaled-up sprite maintains its symmetry by filling in any black missing pixels.

def main(input_grid):
    output_size = 2 * input_grid.shape[0], 2 * input_grid.shape[1]  # scaled up grid
    output_grid = np.zeros(output_size, dtype=int)
    
    sym = detect_rotational_symmetry(input_grid, ignore_colors=[Color.BLACK])
    
    colored_pixels = np.argwhere(input_grid != Color.BLACK)
    
    for x, y in colored_pixels:
        color = input_grid[x, y]

        for i in range(2):
            for j in range(2):
                output_grid[2*x + i, 2*y + j] = color

    scaled_colored_pixels = np.argwhere(output_grid != Color.BLACK)
    
    for x, y in scaled_colored_pixels:
        color = output_grid[x, y]

        for i in range(4):
            rotated_x, rotated_y = sym.apply(x//2, y//2, iters=i)
            scaled_rotated_x, scaled_rotated_y = 2 * rotated_x, 2 * rotated_y
            
            for dx in range(2):
                for dy in range(2):
                    if output_grid[scaled_rotated_x + dx, scaled_rotated_y + dy] == Color.BLACK:
                        output_grid[scaled_rotated_x + dx, scaled_rotated_y + dy] = color
                    else:
                        assert output_grid[scaled_rotated_x + dx, scaled_rotated_y + dy] == color, "The object is not symmetric after scaling"

    return output_grid


def generate_input():
    n, m = random.randint(4, 6), random.randint(4, 6)
    
    # Initialize empty grid of 10x10 to allow some randomness
    grid = np.zeros((10, 10), dtype=int)
    
    # Create a symmetric sprite with missing parts
    sprite = random_sprite(n, n, density=0.5, symmetry="radial", color_palette=list(Color.NOT_BLACK))
    
    # Randomly remove some pixels
    for i in range(sprite.shape[0]):
        for j in range(sprite.shape[1]):
            if random.random() < 0.2:
                sprite[i, j] = Color.BLACK
    
    x, y = random_free_location_for_sprite(grid, sprite)
    blit_sprite(grid, sprite, x, y)
    
    return grid