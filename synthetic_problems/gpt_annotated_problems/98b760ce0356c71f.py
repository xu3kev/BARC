from common import *

import numpy as np
from typing import *

# concepts:
# cropping, objects, connectivity, flood fill

# description:
# In the input, you will see a 15x15 grid with several colored shapes of various sizes floating on a black background.
# To make the output, identify the largest connected component (ignoring black), crop it out of the background, 
# and then flood fill all pixels that are not part of this shape with the color grey.

def main(input_grid):
    # Find all non-black connected components
    components = find_connected_components(input_grid, background=Color.BLACK, connectivity=8, monochromatic=False)
    
    # Identify the largest component
    largest_component = max(components, key=lambda c: c.size)
    
    # Crop the largest component
    cropped = crop(largest_component, background=Color.BLACK)
    
    # Create output grid of the same size as the cropped component
    output_grid = np.full_like(cropped, Color.GREY)
    
    # Copy the largest component onto the output grid
    output_grid[cropped != Color.BLACK] = cropped[cropped != Color.BLACK]
    
    return output_grid

def generate_input():
    # Create a 15x15 black grid
    grid = np.full((15, 15), Color.BLACK)
    
    # Generate 3-5 random sprites of various sizes
    num_sprites = np.random.randint(3, 6)
    for _ in range(num_sprites):
        w = np.random.randint(3, 8)
        h = np.random.randint(3, 8)
        sprite = random_sprite(w, h, color_palette=Color.NOT_BLACK)
        
        # Place sprite at a random free location
        x, y = random_free_location_for_sprite(grid, sprite, padding=1)
        blit_sprite(grid, sprite, x, y)
    
    return grid