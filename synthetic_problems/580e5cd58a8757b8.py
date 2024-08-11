from common import *

import numpy as np
from typing import *


# Concepts: Reflection Symmetry, Objects, Patterns
# Description:
# In the input grid, you'll find objects consisting of various colored pixels.
# Each object needs to be reflected horizontally across the center line of the grid.
# If an object already lies on the reflection line, its mirror image will be created on the opposite side.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Get the dimensions of the grid
    n, m = input_grid.shape

    # Determine the background color by finding the most common color in the grid
    background_color = np.bincount(input_grid.flatten()).argmax()

    # Find the objects in the grid
    objects = find_connected_components(input_grid, background=background_color, connectivity=8, monochromatic=False)
    
    # Initialize the output grid with the background color
    output_grid = np.full_like(input_grid, background_color)

    # Reflect each object horizontally across the center line
    for obj in objects:
        # Get the bounding box of the object
        x, y, w, h = bounding_box(obj, background=background_color)

        # Crop the object from input_grid
        cropped_obj = obj[x:x+w, y:y+h]
        
        # Reflect the object horizontally
        reflected_obj = np.fliplr(cropped_obj)
        
        # Position to place the reflected object in the output grid
        reflected_x = x
        reflected_y = m - y - h
        
        # Blit both the original and reflected objects into the output grid
        blit(output_grid, cropped_obj, x, y, background=background_color)
        blit(output_grid, reflected_obj, reflected_x, reflected_y, background=background_color)

    return output_grid

def generate_input():
    # Define the size of the grid
    n, m = np.random.randint(10, 30), np.random.randint(10, 30)
    grid = np.full((n, m), Color.BLACK)

    # Define the number of objects
    num_objects = np.random.randint(2, 5)
    
    for _ in range(num_objects):
        # Generate a random object
        color = random.choice(Color.NOT_BLACK)
        object_width = np.random.randint(2, m // 2)
        object_height = np.random.randint(2, n // 2)
        obj = random_sprite(object_height, object_width, density=0.7, color_palette=[color])
        
        # Find a random location for the object in the grid
        x, y = random_free_location_for_object(grid, obj, background=Color.BLACK, border_size=1, padding=1)
        
        # Place the object in the grid
        blit(grid, obj, x, y, background=Color.BLACK)

    return grid