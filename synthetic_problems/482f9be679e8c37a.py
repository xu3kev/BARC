from common import *

import numpy as np
from typing import *

# concepts:
# objects, scaling, alignment by color

# description:
# In the input, you will see several objects of different colors and sizes scattered on a grid. Each object contains a special black pixel.
# The output should be a grid where each object is scaled to a fixed size, while maintaining its original shape and color pattern.
# Each object should be centered at the position of its special black pixel in the original input, and that pixel should remain black.

def scale_object(sprite, new_size):
    """
    Scale the object to the new_size.
    """
    old_size = sprite.shape[0]
    factor = new_size // old_size
    scaled_sprite = np.kron(sprite, np.ones((factor, factor), dtype=int))
    return scaled_sprite

def main(input_grid: np.ndarray) -> np.ndarray:
    # Find all the objects on the input grid
    objects = find_connected_components(input_grid, monochromatic=False, connectivity=8)

    # Extract sprites for each object
    sprites = [crop(obj, background=Color.BLACK) for obj in objects]

    # Make a large enough output grid
    output_grid = np.copy(input_grid)
    
    # Define new fixed size for scaling (e.g., scaling each object to 5x5)
    new_size = 5

    for sprite in sprites:
        # Find the special black pixel
        black_pixel_x, black_pixel_y = np.argwhere(sprite == Color.BLACK)[0]

        # Scale the sprite while keeping the black pixel position
        scaled_sprite = scale_object(sprite, new_size)

        # Calculate the center position of the scaled sprite for alignment
        center_x, center_y = new_size // 2, new_size // 2
        
        # Determine the new top-left position to align the black pixel and avoid overflow
        top_left_x = black_pixel_x - center_x
        top_left_y = black_pixel_y - center_y

        # Calculate position to fit the new scaled sprite in the output grid
        grid_x = top_left_x + black_pixel_x
        grid_y = top_left_y + black_pixel_y

        # Blit the scaled sprite into the output grid
        blit_sprite(output_grid, scaled_sprite, x=grid_x, y=grid_y, background=Color.BLACK)

    return output_grid


def generate_input() -> np.ndarray:
    # Create an empty grid
    n, m = 10, 10
    grid = np.full((n, m), Color.BLACK)

    # Define a palette of colors for the different objects
    colors = list(Color.NOT_BLACK)
    
    # Generate random objects and place them in the grid
    num_objects = np.random.randint(2, 5)
    for _ in range(num_objects):
        size = np.random.randint(2, 4)
        color = np.random.choice(colors)
        sprite = random_sprite(size, size, density=1, symmetry="not_symmetric", color_palette=[color])
        
        # Place a special black pixel in the object
        special_x, special_y = np.random.randint(0, size), np.random.randint(0, size)
        sprite[special_x, special_y] = Color.BLACK
        
        # Place the object in the grid randomly
        x, y = random_free_location_for_sprite(grid, sprite, padding=1)
        blit_sprite(grid, sprite, x, y, background=Color.BLACK)

    return grid