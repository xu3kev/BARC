import numpy as np
from typing import *
from common import *

# concepts:
# objects, resizing, color, pixel manipulation

# description:
# In the input grid, you will see several scattered clusters of colored pixels, each representing an object.
# To make the output:
# 1. Double the size of each object, preserving the shape and colors.
# 2. Ensure the output grid is resized proportionally to fit all objects without losing any.
# 3. Arrange the enlarged objects in the output grid, avoiding overlap.

def main(input_grid):
    # Get the connected components (objects) from the input grid
    objects = find_connected_components(input_grid, monochromatic=False, connectivity=8)

    # Crop the objects to their smallest bounding box
    sprites = [crop(obj) for obj in objects]
    
    # Define the scaling factor
    scale_factor = 2

    # Determine the new size for each sprite
    resized_sprites = []
    for sprite in sprites:
        # Get the dimensions of the current sprite
        original_height, original_width = sprite.shape
        # Calculate the new dimensions
        new_height, new_width = original_height * scale_factor, original_width * scale_factor
        # Create an empty grid for the resized sprite
        new_sprite = np.full((new_height, new_width), Color.BLACK)
        # Fill in the new sprite by scaling each pixel
        for i in range(original_height):
            for j in range(original_width):
                if sprite[i, j] != Color.BLACK:
                    new_sprite[i*scale_factor:(i+1)*scale_factor, j*scale_factor:(j+1)*scale_factor] = sprite[i, j]
        resized_sprites.append(new_sprite)
    
    # Calculate the necessary output grid size
    max_width = sum(sprite.shape[1] for sprite in resized_sprites)
    max_height = sum(sprite.shape[0] for sprite in resized_sprites)
    output_grid = np.full((max_height, max_width), Color.BLACK)
    
    # Place the enlarged sprites in the output grid without overlapping
    current_x, current_y = 0, 0
    for sprite in resized_sprites:
        sprite_height, sprite_width = sprite.shape
        if current_x + sprite_height > max_height:
            current_x = 0
            current_y += sprite_width
        blit_sprite(output_grid, sprite, current_x, current_y, background=Color.BLACK)
        current_x += sprite_height
    
    # Crop the final output grid to remove any unnecessary black background
    output_grid = crop(output_grid, background=Color.BLACK)

    return output_grid


def generate_input():
    # Define the grid dimensions
    n = np.random.randint(20, 30)
    m = np.random.randint(20, 30)
    grid = np.full((n, m), Color.BLACK)
    
    # Create a list of random colored objects
    num_objects = np.random.randint(3, 6)
    objects = []
    for _ in range(num_objects):
        obj_width = np.random.randint(1, 4)
        obj_height = np.random.randint(1, 4)
        sprite = random_sprite(obj_height, obj_width, density=0.5, color_palette=Color.NOT_BLACK)
        objects.append(sprite)
    
    # Place the objects randomly on the grid
    for obj in objects:
        obj_height, obj_width = obj.shape
        x, y = random_free_location_for_sprite(grid, obj, padding=1, border_size=1, background=Color.BLACK)
        blit_sprite(grid, obj, x, y)
    
    return grid