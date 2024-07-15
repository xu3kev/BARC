from common import *
import numpy as np
from typing import *

# concepts:
# reflection, objects

# description:
# In the input, you will see an object of random shape and color. 
# The task is to reflect this object horizontally to the other side 
# of the grid about its vertical centerline.

def main(input_grid):
    # Find the vertical centerline of the grid
    centerline = input_grid.shape[1] // 2
    
    # Create the output grid with the same size as the input grid
    output_grid = np.copy(input_grid)
    
    # Detect objects in the grid
    objects = detect_objects(input_grid, predicate=None, background=Color.BLACK, monochromatic=False, connectivity=4)
    
    for obj in objects:
        obj_bounding_box = bounding_box(obj)
        x, y, width, height = obj_bounding_box
        
        # Reflect the object about the vertical centerline
        for i in range(width):
            for j in range(height):
                original_x = x + i
                original_y = y + j
                
                # Calculate the new position for the reflected pixel
                reflected_y = 2 * centerline - original_y - 1
                
                output_grid[original_x, reflected_y] = input_grid[original_x, original_y]
                output_grid[original_x, original_y] = Color.BLACK  # Clear the original position
    
    return output_grid

def generate_input():
    # Create a rectangular black grid with dimensions between 10x10 and 20x20
    n = np.random.randint(10, 20)
    m = np.random.randint(10, 20)
    grid = np.full((n, m), Color.BLACK)
    
    # Generate a random object with random shape and color
    obj_width = np.random.randint(2, n//2)
    obj_height = np.random.randint(2, m//2)
    obj = random_sprite(obj_width, obj_height, density=0.5, color_palette=Color.NOT_BLACK, connectivity=4)
    
    # Randomly place the object on the left half of the grid
    x = np.random.randint(0, n - obj_width)
    y = np.random.randint(0, m//2 - obj_height)
    blit(grid, obj, x, y, background=Color.BLACK)
    
    return grid