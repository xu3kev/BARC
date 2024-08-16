from common import *

import numpy as np
from typing import *

# concepts:
# color mapping, objects, counting, connectivity

# description:
# The input is a grid with various colored objects on a black background.
# To make the output, follow these steps:
# 1. Count the number of pixels in each object.
# 2. If the object has an odd number of pixels, change its color according to this mapping:
#    red -> blue, blue -> green, green -> yellow, yellow -> red
# 3. If the object has an even number of pixels, change its color according to this mapping:
#    red -> yellow, blue -> red, green -> blue, yellow -> green
# 4. Any other colors should remain unchanged.

def main(input_grid):
    # Initialize output grid
    output_grid = np.copy(input_grid)

    # Define color mappings
    odd_map = {Color.RED: Color.BLUE, Color.BLUE: Color.GREEN, 
               Color.GREEN: Color.YELLOW, Color.YELLOW: Color.RED}
    even_map = {Color.RED: Color.YELLOW, Color.BLUE: Color.RED, 
                Color.GREEN: Color.BLUE, Color.YELLOW: Color.GREEN}

    # Find connected components (objects)
    objects = find_connected_components(input_grid, background=Color.BLACK)

    for obj in objects:
        # Count pixels in the object
        pixel_count = np.sum(obj != Color.BLACK)
        
        # Get the original color of the object
        original_color = input_grid[obj != Color.BLACK][0]
        
        # Apply appropriate color mapping based on pixel count
        if pixel_count % 2 == 1:  # Odd number of pixels
            new_color = odd_map.get(original_color, original_color)
        else:  # Even number of pixels
            new_color = even_map.get(original_color, original_color)
        
        # Update the output grid
        output_grid[obj != Color.BLACK] = new_color

    return output_grid

def generate_input():
    # Create a black 10x10 grid as the background
    n, m = 10, 10
    grid = np.zeros((n, m), dtype=int)
    
    # Create a random number of objects
    num_objects = np.random.randint(3, 7)
    colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW]
    
    for _ in range(num_objects):
        # Create a random sprite
        sprite = random_sprite(np.random.randint(2, 5), np.random.randint(2, 5), 
                               symmetry="not_symmetric", 
                               color_palette=[random.choice(colors)])
        
        # Try to place the sprite on the grid
        try:
            x, y = random_free_location_for_sprite(grid, sprite, padding=1, padding_connectivity=8)
            blit_sprite(grid, sprite, x=x, y=y)
        except:
            pass

    return grid