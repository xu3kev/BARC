from common import *

import numpy as np
from typing import *

# concepts:
# edge detection, connectivity, objects

# description:
# In the input, you will see a grid containing multiple objects (different colored regions).
# The task is to outline the edges of each object using a specific color (e.g., Blue).
# The output should be the input grid with the edges of the objects enhanced.

def main(input_grid):
    output_grid = np.copy(input_grid)
    edge_color = Color.BLUE
    object_color = Color.BLACK  # assuming black as the color to transparently detect objects
    
    # Find all connected components (objects)
    objects = find_connected_components(input_grid, background=object_color, connectivity=4, monochromatic=False)

    for obj in objects:
        # Detect the boundary of each object
        boundary_mask = object_boundary(obj, background=object_color)
        x_indices, y_indices = np.where(boundary_mask)
        for x, y in zip(x_indices, y_indices):
            output_grid[x, y] = edge_color  # Change the boundary color to the specified edge color
    
    return output_grid

def generate_input():
    n, m = np.random.randint(12, 20), np.random.randint(12, 20)
    grid = np.full((n, m), Color.BLACK)
    
    n_objects = np.random.randint(3, 6)
    for _ in range(n_objects):
        sprite = random_sprite(np.random.randint(3, 5), np.random.randint(3, 5), color_palette=Color.NOT_BLACK)
        x, y = random_free_location_for_object(grid, sprite, background=Color.BLACK, padding=1)
        blit(grid, sprite, x, y)
    
    return grid