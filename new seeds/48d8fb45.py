from common import *

import numpy as np
from typing import *

# concepts:
# object extraction, indicator detection, cropping

# description:
# In the input you will see several objects with same color placed in a 10x10 grid, only one of 
# them has a gray pixel as an indicator.
# To make the output grid, you should select the object with the gray pixel, crop it, and then output it.

def main(input_grid):
    # Detect all the objects in the input grid.
    obj_list = detect_objects(grid=input_grid, connectivity=8, monochromatic=False, background=Color.BLACK)
    for obj in obj_list:
        cropped_obj = crop(grid=obj)

        # Find the object with gray pixel as an indicator.
        if np.any(cropped_obj == Color.GRAY):
            extracted_obj = cropped_obj
            break
    
    # Seperate the gray pixel and the selected object
    seperate_obj = detect_objects(grid=extracted_obj, connectivity=8, monochromatic=True, background=Color.BLACK)
    for obj in seperate_obj:
        cropped_obj = crop(grid=obj)
        if cropped_obj.shape == (3, 3):
            output_grid = crop(grid=obj)
            break
    
    # Only output the selected object.
    return output_grid
def generate_input():
    # Generate a 10x10 grid with several objects with same color placed in it
    n, m = 10, 10
    grid = np.zeros((n, m), dtype=int)
    
    # Select a color for the objects and the number of objects.
    available_colors = [c for c in Color.NOT_BLACK if c != Color.GRAY]
    obj_color = random.choice(available_colors)
    num_obj = np.random.randint(2,4)

    # Place the objects in the grid.
    for i in range(num_obj):

        # Create a 3x3 object with the selected color and random pattern.
        obj = random_sprite(n=3, m=3, color_palette=[obj_color], density=0.4)

        # Make sure the grey pixel is connected to the object.
        if i == 0:
            obj[1, 0] = obj_color
        
        # Place the object in the grid.
        try:
            x, y = random_free_location_for_sprite(grid=grid, sprite=obj, padding=1, padding_connectivity=8, border_size=1)
        except:
            continue

        # Add Gray pixel to one of the object as an indicator.
        if i == 0:
            grid[x + 1, y - 1] = Color.GRAY

        # Place the object in the grid.
        grid = blit_sprite(x=x, y=y, grid=grid, sprite=obj, background=Color.BLACK)
            
    return grid
# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
