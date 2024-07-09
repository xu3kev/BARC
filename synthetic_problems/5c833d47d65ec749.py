from common import *

import numpy as np
from typing import *

# concepts:
# boundary recognition, interior filling, flood fill

# description:
# In the input, you will see various colored shapes on a black background.
# The output should retain the boundary of the shapes while the interiors are filled with a different color.
# The boundary of a shape retains its original color, while the interior is filled with BLUE.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Create a copy of the input to work on
    output_grid = input_grid.copy()
    
    # Detect all the objects in the grid
    objects = detect_objects(input_grid, background=Color.BLACK, monochromatic=True, connectivity=4)
    
    for obj in objects:
        # Determine the boundary of the object
        boundary = object_boundary(obj, background=Color.BLACK)
        
        # Determine the interior of the object by removing the boundary
        interior = object_interior(obj, background=Color.BLACK)
        interior[boundary] = False

        # Fill the interior with a new color (BLUE)
        output_grid[interior] = Color.BLUE
    
    return output_grid

def generate_input() -> np.ndarray:
    # Randomly generating an input grid
    n, m = np.random.randint(10, 15), np.random.randint(10, 15)
    grid = np.zeros((n, m), dtype=int)

    # Random number of objects
    n_objects = np.random.randint(3, 6)
    colors = list(Color.NOT_BLACK)
    
    for _ in range(n_objects):
        # Randomly create shapes of different sizes
        shape_size = np.random.randint(3, 6)
        color = random.choice(colors)
        shape = random_sprite(shape_size, shape_size, connectivity=4, color_palette=[color])
        
        # Place the shape randomly on the grid
        try:
            x, y = random_free_location_for_object(grid, shape, background=Color.BLACK)
            blit(grid, shape, x, y, background=Color.BLACK)
        except:
            continue

    return grid

# Test the functions