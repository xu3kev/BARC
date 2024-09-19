from common import *

import numpy as np
from typing import *

# concepts:
# object extraction, contact, cropping

# description:
# In the input you will see several objects with same color placed in a 10x10 grid, only one of 
# them contact a gray pixel.
# To make the output grid, you should select the object contact the gray pixel, crop it, and then output it.

def main(input_grid):
    # Get the color of the pattern
    pattern_color = [color for color in np.unique(input_grid) if color != Color.BLACK and color != Color.GRAY][0]

    # Detect all the patterns with pattern color in the input grid
    pattern_list = detect_objects(grid=input_grid, colors=[pattern_color], connectivity=8, monochromatic=True)

    # Detect the indicator gray pixel
    gray_pixel = detect_objects(grid=input_grid, colors=[Color.GRAY], connectivity=8, monochromatic=True)[0]

    # Find out which pattern has contact the gray pixel
    for pattern in pattern_list:
        cropped_pattern = crop(grid=pattern)
        # Check if the gray pixel contact the pattern
        if contact(object1=pattern, object2=gray_pixel, connectivity=4):
            # Crop the pattern and output it
            output_grid = cropped_pattern
            break

    return output_grid

def generate_input():
    # Generate a 10x10 grid with several objects with same color placed in it
    n, m = 10, 10
    grid = np.zeros((n, m), dtype=int)
    
    # Select a color for the objects and the number of objects.
    available_colors = [c for c in Color.NOT_BLACK if c != Color.GRAY]
    obj_color = random.choice(available_colors)
    num_sprite = np.random.randint(2,4)

    # Place the objects in the grid.
    for i in range(num_sprite):
        # Create a 3x3 object with the selected color and random pattern.
        sprite = random_sprite(n=3, m=3, color_palette=[obj_color], density=0.4)
        # Place the object in the grid.
        try:
            x, y = random_free_location_for_sprite(grid=grid, sprite=sprite, padding=1, padding_connectivity=8, border_size=1)
        except:
            continue
        # Add a gray pixel to contact one of the object.
        if i == 0:
            grid[x + 1, y - 1] = Color.GRAY
            # Make sure the grey pixel contact the object.
            grid[x + 1, y] = obj_color
        # Place the object in the grid.
        grid = blit_sprite(x=x, y=y, grid=grid, sprite=sprite, background=Color.BLACK)
            
    return grid
# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
