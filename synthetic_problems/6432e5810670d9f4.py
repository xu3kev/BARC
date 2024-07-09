from common import *

import numpy as np
from typing import *

# concepts:
# patterns, positioning, copying, rotation

# description:
# In the input you will see four square patterns of pixels, one in each corner of the grid. All pixels in the patterns are the same color.
# To make the output, copy each pattern to the corresponding corner of a new grid, but rotate each pattern 90 degrees clockwise.
# The output grid should be the same size as the input grid.

def main(input_grid):
    # Get the patterns from the input
    objects = find_connected_components(input_grid, connectivity=8)

    # Find the bounding box of each pattern
    bounding_boxes = [bounding_box(obj) for obj in objects]

    # Create the output grid with the same size as the input
    n, m = input_grid.shape
    output_grid = np.full((n, m), Color.BLACK)

    # Copy and rotate the patterns to the output grid
    for obj, (x, y, w, h) in zip(objects, bounding_boxes):
        # Crop the pattern to remove any extra rows or columns of black pixels
        sprite = crop(obj)
        
        # Rotate the sprite 90 degrees clockwise
        rotated_sprite = np.rot90(sprite, k=-1)
        
        # Determine the new position for the rotated sprite
        if x < n // 2 and y < m // 2:  # Top-left corner
            new_x, new_y = 0, 0
        elif x < n // 2 and y >= m // 2:  # Top-right corner
            new_x, new_y = 0, m - rotated_sprite.shape[1]
        elif x >= n // 2 and y < m // 2:  # Bottom-left corner
            new_x, new_y = n - rotated_sprite.shape[0], 0
        else:  # Bottom-right corner
            new_x, new_y = n - rotated_sprite.shape[0], m - rotated_sprite.shape[1]
        
        # Copy the rotated pattern to the output grid
        blit_sprite(output_grid, rotated_sprite, x=new_x, y=new_y, background=Color.BLACK)
    
    return output_grid

def generate_input():
    # Make a random sized grid with black background
    n = np.random.randint(8, 12)
    m = np.random.randint(8, 12)
    grid = np.zeros((n, m), dtype=int)

    # Select a color for the patterns
    color = np.random.choice(list(Color.NOT_BLACK))

    # Select a size for the patterns
    size = np.random.randint(2, min(n, m) // 2)

    # Function to create a random pattern
    def create_pattern(size):
        return [[np.random.choice([color, Color.BLACK]) for _ in range(size)] for _ in range(size)]

    # Make random patterns in each corner
    grid[:size, :size] = create_pattern(size)  # Top-left
    grid[:size, -size:] = create_pattern(size)  # Top-right
    grid[-size:, :size] = create_pattern(size)  # Bottom-left
    grid[-size:, -size:] = create_pattern(size)  # Bottom-right

    # Check that at least one of the patterns is not all black
    # If they are all black, try again
    if np.all(grid == Color.BLACK):
        return generate_input()

    return grid