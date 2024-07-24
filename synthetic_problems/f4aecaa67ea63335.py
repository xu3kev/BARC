from common import *

import numpy as np
from typing import *

# concepts:
# boundary identification, connectivity

# description:
# The input grid contains a number of colored objects. The task is to identify the boundaries of these objects
# and highlight the boundary pixels with a specific color (e.g., BLUE). The original object colors will remain unchanged except for their boundaries.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.copy(input_grid)
    background_color = Color.BLACK
    boundary_color = Color.BLUE

    # Find all monochromatic objects in the grid
    objects = detect_objects(input_grid, monochromatic=True, connectivity=8, background=background_color)

    for obj in objects:
        # Compute the boundary of the object
        boundary = object_boundary(obj, background=background_color)
        
        # Highlight the boundary using boundary_color
        for x, y in np.argwhere(boundary):
            output_grid[x, y] = boundary_color

    return output_grid

def generate_input() -> np.ndarray:
    grid_size = np.random.randint(10, 15), np.random.randint(10, 15)
    grid = np.zeros(grid_size, dtype=int)

    num_objects = np.random.randint(3, 7)
    colors = list(Color.NOT_BLACK)
    np.random.shuffle(colors)

    for _ in range(num_objects):
        color = colors.pop()
        sprite_size = np.random.randint(3, 6), np.random.randint(3, 6)
        sprite = random_sprite(*sprite_size, color_palette=[color], background=Color.BLACK)

        x, y = random_free_location_for_object(grid, sprite)
        blit(grid, sprite, x, y)

    return grid