from common import *

import numpy as np
from typing import *

# concepts:
# color, patterns, objects, bounding box

# description:
# In the input, you will see objects colored in grey, and one isolated green pixel as a marker.
# Every grey object includes at least one pixel adjacent to any side of the bounding box defined by the marker.
# In the output grid, color those identified objects blue while keeping other portions black.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Create the output grid that copies input grid
    output_grid = np.copy(input_grid)
    
    # Find the marker (green pixel)
    marker_pos = np.argwhere(input_grid == Color.GREEN)[0]
    marker_x, marker_y = marker_pos

    # Get all grey objects in the input grid
    grey_objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=8)

    # Scan each grey object
    for obj in grey_objects:
        # Get bounding box of the object
        x, y, width, height = bounding_box(obj, background=Color.BLACK)

        # Check if marker is adjacent to the bounding box
        if (x <= marker_x <= x + width and y - 1 <= marker_y <= y + height + 1) or \
           (y <= marker_y <= y + height and x - 1 <= marker_x <= x + width + 1):
            # Change object's color to blue in the output grid
            output_grid[obj == Color.GREY] = Color.BLUE
        else:
            output_grid[obj == Color.GREY] = Color.BLACK

    return output_grid

def generate_input() -> np.ndarray:
    # Make a black 10x10 grid as the background
    n = m = 10
    grid = np.zeros((n, m), dtype=int)
    
    # Make a random number of grey objects (3 to 6)
    num_sprites = np.random.randint(3, 7)
    for _ in range(num_sprites):
        sprite = random_sprite(np.random.randint(2, 4), np.random.randint(2, 4), symmetry="not_symmetric", color_palette=[Color.GREY])
        try:
            x, y = random_free_location_for_sprite(grid, sprite, padding=1, padding_connectivity=8)
            blit_sprite(grid, sprite, x=x, y=y)
        except:
            pass

    # Add a single green pixel as the marker randomly within the grid
    empty_cells = [(i, j) for i in range(n) for j in range(m) if grid[i, j] == Color.BLACK]
    marker_x, marker_y = random.choice(empty_cells)
    grid[marker_x, marker_y] = Color.GREEN

    return grid