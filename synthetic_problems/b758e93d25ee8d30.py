from common import *

import numpy as np
from typing import *

# concepts:
# patterns, positioning, objects, color guide

# description:
# In the input, the grid will contain multiple colored patterns each of which will be repeated in multiple instances across the grid.
# Each colored pattern acts as a guide, indicating where a mono-colored object of the same color should be placed in the output grid.
# The output grid should have one instance of each mono-colored object according to the position indicated by the patterns in the input grid.

def main(input_grid):
    # Prepare output grid
    output_grid = np.zeros_like(input_grid)
    
    # Identify all unique colors in the grid (omitting Color.BLACK)
    unique_colors = np.setdiff1d(np.unique(input_grid), [Color.BLACK])
    
    # For each unique color, identify and position the mono-colored object
    for color in unique_colors:
        if color != Color.BLACK:
            # Get all connected components of the current color
            components = find_connected_components(input_grid, background=Color.BLACK, connectivity=8, monochromatic=True)
            color_components = [comp for comp in components if input_grid[np.where(comp)].flat[0] == color]

            # Use the first component as the pattern guide to determine the position for the mono-colored object
            guide_pattern = color_components[0]
            guide_bbox = bounding_box(guide_pattern)
            
            # Create the mono-colored object
            object_grid = np.where(guide_pattern != Color.BLACK, color, Color.BLACK)
            
            # Randomly place the object onto the output grid
            x, y = random_free_location_for_sprite(output_grid, object_grid, background=Color.BLACK)
            blit_sprite(output_grid, object_grid, x, y)

    return output_grid


def generate_input():
    # Create a random sized grid with black background
    n, m = np.random.randint(10, 16), np.random.randint(10, 16)
    grid = np.zeros((n, m), dtype=int)
    
    # Randomly choose the number of patterns between 3 and 6
    num_patterns = np.random.randint(3, 7)
    
    for _ in range(num_patterns):
        # Choose a random color for the pattern (not black)
        pattern_color = np.random.choice(list(Color.NOT_BLACK))
        
        # Size of the pattern
        pattern_size = np.random.randint(2, 5)

        # Generate a random pattern with the chosen color
        pattern = random_sprite(pattern_size, pattern_size, color_palette=[pattern_color])

        # Ensure the pattern is contiguous
        while not is_contiguous(pattern, connectivity=8):
            pattern = random_sprite(pattern_size, pattern_size, color_palette=[pattern_color])
        
        # Scatter multiple instances of the pattern across the grid,
        # ensuring they do not overlap
        for _ in range(np.random.randint(2, 4)):
            x, y = random_free_location_for_sprite(grid, pattern)
            while contact(object1=grid, object2=pattern, x2=x, y2=y, connectivity=8):
                x, y = random_free_location_for_sprite(grid, pattern)
            blit_sprite(grid, pattern, x, y)
    
    return grid