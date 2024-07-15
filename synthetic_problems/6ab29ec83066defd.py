from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, color matching, geometric transformation

# description:
# The input consists of two separate objects made from different colored pixels - one object is always at the top-left and
# the other is randomly placed somewhere else on the grid.
# The task is to reflect the second object about the y-axis and match the reflection with the first object symmetrically,
# then merge them together. If there's no overlap, just merge them. The result should be the merged object on an otherwise black background.

def main(input_grid):
    # Identify distinct objects
    non_black_pixels = np.argwhere(input_grid != Color.BLACK)
    
    # Extract the first object (from top-left)
    first_object = np.zeros_like(input_grid)
    first_object[input_grid == input_grid[non_black_pixels[0][0], non_black_pixels[0][1]]] = input_grid[non_black_pixels[0][0], non_black_pixels[0][1]]
    
    # Extract the second object
    second_color = input_grid[non_black_pixels[-1][0], non_black_pixels[-1][1]]
    second_object = np.zeros_like(input_grid)
    second_object[input_grid == second_color] = second_color
    
    # Reflect the second object about the y-axis
    reflected_second_object = np.fliplr(second_object)
    
    # Merge the objects
    output_grid = np.zeros_like(input_grid)
    merged_object = ((first_object != Color.BLACK) | (reflected_second_object != Color.BLACK)) * input_grid
    
    output_grid = merged_object
    
    return output_grid

def generate_input():
    n, m = np.random.randint(5, 10, size=2)
    grid = np.zeros((n, m), dtype=int)

    # Create the first object (top-left)
    first_color = random.choice(list(Color.NOT_BLACK))
    obj1_size = np.random.randint(1, min(n, m)//2)
    first_object = random_sprite(obj1_size, obj1_size, color_palette=[first_color])
    blit_sprite(grid, first_object, 0, 0, background=Color.BLACK)
    
    # Create the second object and place it somewhere else randomly
    second_color = random.choice([c for c in Color.NOT_BLACK if c != first_color])
    obj2_size = np.random.randint(1, min(n, m)//2)
    second_object = random_sprite(obj2_size, obj2_size, color_palette=[second_color])
    x, y = random_free_location_for_sprite(grid, second_object, background=Color.BLACK, padding=1, border_size=1)
    while (x, y) == (0, 0):
        x, y = random_free_location_for_sprite(grid, second_object, background=Color.BLACK, padding=1, border_size=1)
    blit_sprite(grid, second_object, x, y, background=Color.BLACK)

    return grid