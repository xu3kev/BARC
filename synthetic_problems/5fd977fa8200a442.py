from common import *

import numpy as np
from typing import *


# concepts:
# symmetry detection, growing, pixel manipulation

# description:
# In the input, you will see an object that is almost rotationally symmetric, some parts might be removed or covered, and each component should be grown by one pixel in all directions
# To make the output, fill in the missing parts to make it rotationally symmetric and then expand it by one pixel in all directions for the completed parts.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = input_grid.copy()

    # Find the rotational symmetry
    sym = detect_rotational_symmetry(input_grid, ignore_colors=[Color.BLACK])

    # Find the colored pixels
    colored_pixels = np.argwhere(input_grid != Color.BLACK)

    # Apply rotations and fill in any missing parts
    for x, y in colored_pixels:
        color = input_grid[x, y]

        for i in range(1, 4):
            rotated_x, rotated_y = sym.apply(x, y, iters=i)
            if output_grid[rotated_x, rotated_y] == Color.BLACK:
                output_grid[rotated_x, rotated_y] = color

    # Find the new colored pixels after completing the symmetry
    colored_pixels = np.argwhere(output_grid != Color.BLACK)

    # Grow the completed parts symmetrically by one pixel in all directions
    growth_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for x, y in colored_pixels:
        color = output_grid[x, y]
        for dx, dy in growth_offsets:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < output_grid.shape[0] and 0 <= new_y < output_grid.shape[1]:
                output_grid[new_x, new_y] = color
    
    return output_grid


def generate_input() -> np.ndarray:
    # Initialize 10x10 grid
    grid = np.zeros((10, 10), dtype=int)

    # Create a 5x5 sprite with radial symmetry
    sprite = random_sprite(
        5, 5, density=0.3, symmetry="radial", color_palette=list(Color.NOT_BLACK)
    )

    # Randomly remove pixels from the sprite
    for i in range(sprite.shape[0]):
        for j in range(sprite.shape[1]):
            if np.random.random() < 0.3:
                sprite[i, j] = Color.BLACK

    # Place sprite randomly on the grid
    x, y = random_free_location_for_sprite(grid, sprite, border_size=0)
    blit_sprite(grid, sprite, x, y)

    return grid