from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, rotation, pixel manipulation

# description:
# In the input you will see a grid with a symmetric pattern. The symmetry could be horizontal, vertical, or radial.
# To make the output:
# 1. Extract the bounding box around the symmetric object.
# 2. Rotate the object 90 degrees clockwise.
# 3. Place the rotated object back into the same position as the original.
# 4. Extend the borders of the rotated object diagonally with green pixels until hitting the edges of the grid or another colored pixel.

def main(input_grid):
    # find the connected components in the input grid
    components = find_connected_components(input_grid, connectivity=8, monochromatic=False)
    
    # assume there is only one object in the grid (as described)
    main_object = components[0]

    # find the bounding box of the object
    x, y, w, h = bounding_box(main_object)

    # extract the symmetry pattern from the grid
    symmetric_pattern = input_grid[x:x+w, y:y+h]

    # rotate the symmetric pattern 90 degrees clockwise
    rotated_pattern = np.rot90(symmetric_pattern, -1)

    # create an output grid initialized with black
    output_grid = np.copy(input_grid)
    
    # place the rotated pattern back into the same position as the original
    output_grid[x:x+w, y:y+h] = rotated_pattern

    # Extending the borders of the object diagonally with green pixels
    dx_dy = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
    green = Color.GREEN

    for i in range(x, x+w):
        for j in range(y, y+h):
            if rotated_pattern[i-x, j-y] != Color.BLACK:
                for dx, dy in dx_dy:
                    k = 1
                    while True:
                        if 0 <= i+k*dx < output_grid.shape[0] and 0 <= j+k*dy < output_grid.shape[1]:
                            if output_grid[i+k*dx, j+k*dy] == Color.BLACK:
                                output_grid[i+k*dx, j+k*dy] = green
                                k += 1
                            else:
                                break
                        else:
                            break

    return output_grid

def generate_input():
    # choose the color of the sprite
    color = np.random.choice(Color.NOT_BLACK)
    
    # choose the dimensions of the grid
    grid_size = np.random.randint(10, 15)
    grid = np.zeros((grid_size, grid_size), dtype=int)
    
    # choose the symmetrical type and dimensions of the symmetric object
    symmetries = ['horizontal', 'vertical', 'radial']
    symmetry = np.random.choice(symmetries)
    pattern_size = np.random.randint(3, grid_size//2)
    
    symmetric_pattern = random_sprite(pattern_size, pattern_size, density=1, symmetry=symmetry, color_palette=[color])

    # randomly placing the symmetrical pattern in the input grid
    x, y = random_free_location_for_sprite(grid, symmetric_pattern, padding=1, background=Color.BLACK)
    blit_sprite(grid, symmetric_pattern, x, y)

    return grid