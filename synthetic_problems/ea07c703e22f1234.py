from common import *

import numpy as np
from typing import *

# concepts:
# color mapping, connectivity, objects, reflection

# description:
# The input grid contains connected components of different colors on a black background.
# The components can have any shape but are not contiguous.
# To make the output, reflect each component about its vertical axis and map its color based on a specific color mapping.

def main(input_grid):
    # Initialize output grid
    output_grid = np.zeros_like(input_grid)
    
    # Get the connected components 
    components = find_connected_components(input_grid, background=Color.BLACK, connectivity=4, monochromatic=True)
    
    for component in components:
        # Reflect the component about its vertical axis
        reflected_component = np.fliplr(component)
        
        # Get the color of the component (all pixels in a monochromatic component should have the same color)
        original_color = input_grid[component != 0][0]
        new_color = color_map.get(original_color, original_color)
        
        # Paint the reflected component onto the output grid with the new color
        output_grid[reflected_component != 0] = new_color
    
    return output_grid

# Constructing the color map
color_map = {Color.GREEN : Color.YELLOW, 
             Color.BLUE : Color.GRAY, 
             Color.RED : Color.PINK,
             Color.TEAL : Color.MAROON,
             Color.YELLOW : Color.GREEN, 
             Color.GRAY : Color.BLUE, 
             Color.PINK : Color.RED,
             Color.MAROON : Color.TEAL             
            }

def generate_input():
    # Generate random grid dimensions between 5x5 and 10x10
    n, m = np.random.randint(5, 11), np.random.randint(5, 11)
    grid = np.zeros((n, m), dtype=int)
    
    # Add random colored components
    num_components = np.random.randint(3, 8)
    for _ in range(num_components):
        max_size = np.random.randint(2, 4)
        sprite = random_sprite(max_size, max_size, color_palette=list(color_map.keys()))
        try:
            x, y = random_free_location_for_sprite(grid, sprite, border_size=1, padding=1)
            blit_sprite(grid, sprite, x, y)
        except:
            continue
    
    return grid