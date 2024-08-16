from common import *

import numpy as np
from typing import *

# concepts:
# objects, pixel manipulation, connectivity

# description:
# In the input, you will see a set of objects, each consisting of connected pixels of the same color.
# To make the output, for each object:
# 1. Find all pixels that have exactly two neighboring pixels of the same color (diagonal neighbors count).
# 2. Change these pixels to black.
# 3. Expand the remaining pixels of the object outward by one pixel in all directions (including diagonals),
#    but do not overwrite pixels of other colors.

def main(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.zeros_like(input_grid)
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=8, monochromatic=True)

    for obj in objects:
        color = np.max(obj)  # Get the color of the object
        transformed_object = np.zeros_like(obj)

        # Step 1 & 2: Find pixels with exactly two neighbors and set them to black
        for x in range(obj.shape[0]):
            for y in range(obj.shape[1]):
                if obj[x, y] == color:
                    neighbors = obj[max(0, x-1):min(x+2, obj.shape[0]), max(0, y-1):min(y+2, obj.shape[1])]
                    if np.sum(neighbors == color) == 3:  # 3 because it counts the pixel itself
                        transformed_object[x, y] = Color.BLACK
                    else:
                        transformed_object[x, y] = color

        # Step 3: Expand the remaining pixels outward
        expanded_object = np.zeros_like(obj)
        for x in range(obj.shape[0]):
            for y in range(obj.shape[1]):
                if transformed_object[x, y] == color:
                    expansion_area = expanded_object[max(0, x-1):min(x+2, obj.shape[0]), max(0, y-1):min(y+2, obj.shape[1])]
                    expansion_area[expansion_area == Color.BLACK] = color

        # Blit the expanded object onto the output grid
        blit_object(output_grid, expanded_object, background=Color.BLACK)

    return output_grid

def generate_input():
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.full((n, m), Color.BLACK)

    n_objects = np.random.randint(2, 4)

    for _ in range(n_objects):
        color = random.choice(list(Color.NOT_BLACK))
        
        # Generate a random blob-like shape
        obj_size = np.random.randint(4, 8)
        obj = np.zeros((obj_size, obj_size), dtype=int)
        center = obj_size // 2
        obj[center, center] = color

        for _ in range(obj_size * obj_size // 2):
            x, y = np.random.randint(0, obj_size), np.random.randint(0, obj_size)
            if np.any(obj[max(0, x-1):min(x+2, obj_size), max(0, y-1):min(y+2, obj_size)] == color):
                obj[x, y] = color

        # Place the object randomly on the grid
        try:
            x, y = random_free_location_for_sprite(grid, obj, background=Color.BLACK, padding=2, padding_connectivity=8, border_size=2)
            blit_sprite(grid, obj, x=x, y=y, background=Color.BLACK)
        except:
            continue

    # Make sure we actually generated something
    if np.all(grid == Color.BLACK):
        return generate_input()
    
    return grid