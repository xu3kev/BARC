from common import *
import numpy as np
import random

# concepts:
# objects, translating

# description:
# In the input grid, you will see various objects of different colors. 
# To create the output grid, you will translate each object to a new location based on a predefined translation vector.

def main(input_grid):
    # Define the translation vector
    translation_vector = (3, 2)
    
    # Detect objects in the grid
    objects = find_connected_components(input_grid, connectivity=8, monochromatic=False)
    
    # Create a blank output grid
    output_grid = np.zeros_like(input_grid)
    
    # Translate each object
    for obj in objects:
        # Find the bounding box and position of the object
        bbox = bounding_box(obj, background=Color.BLACK)
        obj = crop(obj, background=Color.BLACK)
        obj_x, obj_y = bbox[0], bbox[1]
        
        # Calculate the new position
        new_x = obj_x + translation_vector[0]
        new_y = obj_y + translation_vector[1]
        
        # Ensure the object stays within bounds
        if new_x + obj.shape[0] <= output_grid.shape[0] and new_y + obj.shape[1] <= output_grid.shape[1]:
            blit(output_grid, obj, x=new_x, y=new_y, background=Color.BLACK)
    
    return output_grid

def generate_input():
    # Create a random sized black grid
    n = np.random.randint(10, 15)
    m = np.random.randint(10, 15)
    grid = np.zeros((n, m), dtype=int)
    
    # Number of objects to create
    num_objects = np.random.randint(3, 6)
    
    for _ in range(num_objects):
        # Create a random monochromatic object
        obj_n = obj_m = np.random.randint(2, 5)
        color = np.random.choice(list(Color.NOT_BLACK))
        object_grid = random_sprite(obj_n, obj_m, density=0.6, color_palette=[color], connectivity=8)

        # Attempt to place the object in the grid
        try:
            x, y = random_free_location_for_object(grid, object_grid)
            blit(grid, object_grid, x, y, background=Color.BLACK)
        except ValueError:
            pass # Couldn't place the object, continue without placing
    
    return grid