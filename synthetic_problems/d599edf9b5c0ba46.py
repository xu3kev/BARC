from common import *

import numpy as np
from typing import *

# concepts:
# objects, color guide, masking, scaling, repeating pattern

# description:
# In the input you will see two objects: a large monochromatic object and a smaller multi-colored square.
# To make the output:
# 1. Downscale the large object so that it is the same size as the small multi-colored square.
# 2. Use the downscaled large object as a binary mask to select pixels from the multi-colored square.
# 3. For each selected pixel, create a small square of that color centered on the pixel's position.
# 4. The size of these small squares should be such that they touch but do not overlap.
# The result will be a pixelated version of the masked multi-colored square.

def main(input_grid):
    objects = find_connected_components(input_grid, connectivity=8, monochromatic=False)
    
    # Identify the pattern and the multi-colored square
    pattern = square = None
    for obj in objects:
        if len(set(obj.flatten())) == 2:
            pattern = obj
        else:
            square = obj
    
    # Extract the square sprite
    x, y, width, height = bounding_box(square)
    square_sprite = square[x:x+width, y:y+height]

    # Extract and scale down the pattern
    x2, y2, width2, height2 = bounding_box(pattern)
    width2 = height2 = max(width2, height2)
    pattern_sprite = pattern[x2:x2+width2, y2:y2+height2]
    scale = width2 // width
    scaled_pattern = np.zeros_like(square_sprite)
    for i in range(width):
        for j in range(height):
            scaled_pattern[i,j] = pattern_sprite[i * scale, j * scale]
    
    # Create the pixelated output
    output_size = width * 3  # Each pixel becomes a 3x3 square
    output_grid = np.full((output_size, output_size), Color.BLACK)
    
    for i in range(width):
        for j in range(height):
            if scaled_pattern[i, j]:
                color = square_sprite[i, j]
                output_grid[i*3:i*3+3, j*3:j*3+3] = color
    
    return output_grid

def generate_input():
    size = np.random.randint(4, 7)
    square = random_sprite(size, size, density=1, symmetry="not_symmetric", color_palette=Color.NOT_BLACK)
    
    if len(set(square.flatten())) == 1:
        return generate_input()

    color = np.random.choice(list(Color.NOT_BLACK))
    pattern = random_sprite(size, size, density=.7, symmetry="not_symmetric", color_palette=[color], connectivity=8)

    if not is_contiguous(pattern, connectivity=8):
        return generate_input()

    scale = np.random.randint(3, 7)
    pattern = np.repeat(np.repeat(pattern, scale, axis=0), scale, axis=1)

    n = m = (size * scale) + (2 * size) + np.random.randint(2, 5)
    grid = np.zeros((n, m), dtype=int)

    x, y = np.random.randint(0, n - size * scale), np.random.randint(0, m - size * scale)
    blit_sprite(grid, pattern, x=x, y=y)

    x2, y2 = random_free_location_for_sprite(grid, square)
    while contact(object1=grid, object2=square, x2=x2, y2=y2, connectivity=8):
        x2, y2 = random_free_location_for_sprite(grid, square)
    blit_sprite(grid, square, x=x2, y=y2)

    return grid