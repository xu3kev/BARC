from common import *

import numpy as np
from typing import *

# concepts:
# border detection, color change

# description:
# In the input grid, you will see various multicolored objects scattered around.
# Some of these objects touch the border of the grid.
# The task is to change the color of the objects touching the border to red.

def main(input_grid: np.ndarray) -> np.ndarray:
    objects = find_connected_components(input_grid, connectivity=8, monochromatic=False)
    output_grid = input_grid.copy()
    
    # Identify and change the colors of the objects touching the border
    for obj in objects:
        bounding_coords = np.argwhere(obj != Color.BLACK)
        if any(x == 0 or y == 0 or x == obj.shape[0]-1 or y == obj.shape[1]-1 for x, y in bounding_coords):
            obj_mask = obj != Color.BLACK
            obj[obj_mask] = Color.RED
        blit(output_grid, obj, background=Color.BLACK)

    return output_grid

def generate_input() -> np.ndarray:
    n = np.random.randint(10, 20)
    m = np.random.randint(10, 20)
    input_grid = np.full((n, m), Color.BLACK)
    
    def random_object():
        size_x, size_y = np.random.randint(2, 5), np.random.randint(2, 5)
        obj = np.full((size_x, size_y), np.random.choice(list(Color.NOT_BLACK)))
        for _ in range(size_x * size_y // 2):  # Make sure we have at least one hole
            ix, iy = np.random.randint(size_x), np.random.randint(size_y)
            obj[ix, iy] = Color.BLACK
        return obj
    
    num_objects = np.random.randint(5, 10)
    
    for _ in range(num_objects):
        obj = random_object()
        try:
            x, y = random_free_location_for_object(input_grid, obj, padding=1)
            blit(input_grid, obj, x, y)
        except ValueError:
            pass  # Try again if there's no place left
    
    return input_grid