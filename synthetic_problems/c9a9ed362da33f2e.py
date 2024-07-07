from common import *

import numpy as np
from typing import *

# Concepts:
# objects, boundary highlighting

# Description:
# In the input grid, you will see various colored objects. Each object may have different shapes and colors.
# To create the output grid, copy the input grid. Then, change the color of all border pixels of each object to a different color (for instance, change the border to red).

def main(input_grid):
    # Make a copy of the input grid to work on
    output_grid = input_grid.copy()
    
    # Detect all the objects in the grid
    objects = find_connected_components(input_grid, connectivity=4)
    
    for obj in objects:
        color = np.unique(obj[obj != Color.BLACK])[0]  # assuming each object is monochromatic
        
        # Find the border of the object
        border = object_boundary(obj, background=Color.BLACK)
        
        # Change the border color to a different color (e.g., RED)
        output_grid[border] = Color.RED

    return output_grid

def generate_input():
    # Create a medium sized grid
    n, m = np.random.randint(10, 15), np.random.randint(10, 15)
    input_grid = np.full((n, m), Color.BLACK)

    num_objects = np.random.randint(3, 6)
    for _ in range(num_objects):
        obj_size = np.random.randint(3, 5), np.random.randint(3, 5)
        obj_color = np.random.choice(Color.NOT_BLACK)
        obj = random_sprite(obj_size[0], obj_size[1], density=0.6, color_palette=[obj_color])
        
        try:
            x, y = random_free_location_for_object(input_grid, obj, padding=1)
            blit(input_grid, obj, x, y)
        except ValueError:
            pass  # if it doesn't fit, just skip adding this object

    return input_grid