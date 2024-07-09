from common import *

import numpy as np
from typing import *

# concepts:
# translational symmetry, symmetry detection, objects, copying

# description:
# In the input, you will see a grid containing two different colored sprites (blue and red) that are each repeatedly translated horizontally, forming two rows of the same sprites.
# To make the output, detect the translational symmetry of each row separately. Then, create a new grid that is 9x9. In this grid, continue the horizontal pattern for the blue sprites in rows 1-3 and 7-9, and for the red sprites in rows 4-6. Finally, apply vertical mirroring to the entire grid.

def main(input_grid):
    # Find the blue and red objects
    blue_objects = find_connected_components(input_grid, background=Color.BLACK)
    blue_objects = [obj for obj in blue_objects if np.any(obj == Color.BLUE)]
    red_objects = find_connected_components(input_grid, background=Color.BLACK)
    red_objects = [obj for obj in red_objects if np.any(obj == Color.RED)]

    # Detect translational symmetry for blue and red rows separately
    blue_symmetries = detect_translational_symmetry(input_grid[0:3, :], ignore_colors=[Color.RED, Color.BLACK])
    red_symmetries = detect_translational_symmetry(input_grid[3:6, :], ignore_colors=[Color.BLUE, Color.BLACK])

    # Create the output grid
    output_grid = np.full((9, 9), Color.BLACK)

    # Function to apply horizontal pattern
    def apply_horizontal_pattern(row_start, row_end, objects, symmetries):
        for obj in objects:
            for x, y in np.argwhere(obj != Color.BLACK):
                for x2, y2 in orbit(output_grid[row_start:row_end, :], x, y, symmetries):
                    output_grid[row_start + x2, y2] = obj[x, y]

    # Apply blue pattern to rows 1-3 and 7-9
    apply_horizontal_pattern(0, 3, blue_objects, blue_symmetries)
    apply_horizontal_pattern(6, 9, blue_objects, blue_symmetries)

    # Apply red pattern to rows 4-6
    apply_horizontal_pattern(3, 6, red_objects, red_symmetries)

    # Apply vertical mirroring to the entire grid
    output_grid = np.flipud(output_grid)

    return output_grid

def generate_input():
    # Create a 6x6 grid
    grid = np.full((6, 6), Color.BLACK)

    # Generate blue sprite
    blue_sprite = random_sprite(3, np.random.randint(2, 4), symmetry="not_symmetric", color_palette=[Color.BLUE], density=0.5, connectivity=8)
    
    # Generate red sprite
    red_sprite = random_sprite(3, np.random.randint(2, 4), symmetry="not_symmetric", color_palette=[Color.RED], density=0.5, connectivity=8)

    # Apply horizontal tiling for blue sprite in first 3 rows
    blue_tiled = np.tile(blue_sprite, (1, 3))[:, :6]
    grid[:3, :] = blue_tiled

    # Apply horizontal tiling for red sprite in last 3 rows
    red_tiled = np.tile(red_sprite, (1, 3))[:, :6]
    grid[3:, :] = red_tiled

    return grid