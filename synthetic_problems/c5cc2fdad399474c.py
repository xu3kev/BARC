from common import *

import numpy as np
from typing import *

# concepts:
# color guide, objects, symmetry, filling

# description:
# In the input, you will see a colored object in the middle and two single pixels of different colors in opposite corners (top-left and bottom-right).
# To make the output:
# 1. Remove the two corner pixels.
# 2. Create a symmetrical copy of the central object, mirrored diagonally.
# 3. Color the original object with the color from the top-left pixel.
# 4. Color the mirrored copy with the color from the bottom-right pixel.

def main(input_grid):
    # Copy the input grid to the output grid
    output_grid = np.copy(input_grid)

    # Get the colors of the pixels in the corners
    color1 = output_grid[0, 0]  # Top-left corner
    color2 = output_grid[-1, -1]  # Bottom-right corner

    # Remove the corner pixels
    output_grid[0, 0] = Color.BLACK
    output_grid[-1, -1] = Color.BLACK

    # Find the central object
    object_mask = output_grid != Color.BLACK

    # Create a diagonal mirror of the object
    mirrored_object = np.flipud(np.fliplr(output_grid))

    # Color the original object with color1
    output_grid[object_mask] = color1

    # Color the mirrored object with color2, but only where it doesn't overlap with the original
    mirrored_mask = (mirrored_object != Color.BLACK) & ~object_mask
    output_grid[mirrored_mask] = color2

    return output_grid

def generate_input():
    # Make a square black grid
    n = np.random.randint(9, 15)
    grid = np.zeros((n, n), dtype=int)

    # Select two different colors for the corner pixels
    colors = np.random.choice(list(Color.NOT_BLACK), 2, replace=False)

    # Select a color for the sprite (different from corner colors)
    sprite_color = np.random.choice([c for c in Color.NOT_BLACK if c not in colors])

    # Make random sprite and put it in the middle of the grid
    sprite_size = n // 2
    sprite = random_sprite(sprite_size, sprite_size, symmetry="not_symmetric", color_palette=[sprite_color])
    blit_sprite(grid, sprite, x=(n-sprite_size)//2, y=(n-sprite_size)//2)

    # Put single pixels in the top-left and bottom-right corners
    grid[0, 0] = colors[0]
    grid[-1, -1] = colors[1]

    return grid