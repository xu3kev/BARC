from common import *

import numpy as np
from typing import *

# concepts:
# objects, symmetry detection, alignment by color

# description:
# In the input, you will see several objects scattered on a black grid. Each object is made of two colors: 
# one main color and one accent color (a single pixel).
# To make the output, identify objects with rotational symmetry (90, 180, or 270 degrees).
# For each symmetric object, place it in the output grid such that its accent pixel aligns with the center.
# The output grid should be the smallest possible size that contains all the symmetric objects 
# (after they have been placed correctly), which for all inputs here is 5x5.

def main(input_grid):
    # Extract the objects from the input
    objects = find_connected_components(input_grid, monochromatic=False, connectivity=8)

    # Convert the objects into sprites by cropping them
    sprites = [crop(obj, background=Color.BLACK) for obj in objects]

    # Filter for rotationally symmetric sprites
    symmetric_sprites = []
    for sprite in sprites:
        if (np.array_equal(sprite, np.rot90(sprite, 1)) or 
            np.array_equal(sprite, np.rot90(sprite, 2)) or 
            np.array_equal(sprite, np.rot90(sprite, 3))):
            symmetric_sprites.append(sprite)

    # Create output grid
    output_grid = np.full((5, 5), Color.BLACK)

    # Place each symmetric sprite into the output grid
    for sprite in symmetric_sprites:
        # Find the accent pixel (the one that's different from the main color)
        main_color = np.argmax(np.bincount(sprite.flatten())[1:]) + 1
        accent_pixel_x, accent_pixel_y = np.argwhere(sprite != main_color)[0]

        # Calculate the offset to ensure the accent pixel ends up in the center
        center_x, center_y = output_grid.shape[0] // 2, output_grid.shape[1] // 2
        x, y = center_x - accent_pixel_x, center_y - accent_pixel_y
        
        # Place the sprite into the output grid
        blit_sprite(output_grid, sprite, x, y, background=Color.BLACK)

    return output_grid

def generate_input():
    # Create a series of objects, some with rotational symmetry and some without
    sprites = []

    n_objects = np.random.randint(3, 6)
    for _ in range(n_objects):
        # Randomly decide if this sprite will be symmetric
        is_symmetric = np.random.choice([True, False])
        
        if is_symmetric:
            # Create a rotationally symmetric sprite
            size = np.random.randint(3, 5)
            main_color = random.choice(list(Color.NOT_BLACK))
            accent_color = random.choice([c for c in Color.NOT_BLACK if c != main_color])
            
            sprite = np.full((size, size), main_color)
            
            # Add accent pixel ensuring symmetry
            if size % 2 == 1:  # Odd size
                sprite[size//2, size//2] = accent_color
            else:  # Even size
                sprite[size//2-1:size//2+1, size//2-1:size//2+1] = accent_color
        else:
            # Create a non-symmetric sprite
            sprite = random_sprite(np.random.randint(3, 5), np.random.randint(3, 5), 
                                   color_palette=random.sample(list(Color.NOT_BLACK), 2),
                                   symmetry="not_symmetric")

        sprites.append(sprite)

    # Place the sprites randomly on a medium sized canvas
    n, m = np.random.randint(15, 25), np.random.randint(15, 25)
    grid = np.full((n, m), Color.BLACK)
    for sprite in sprites:
        x, y = random_free_location_for_sprite(grid, sprite, padding=1, padding_connectivity=8)
        blit_sprite(grid, sprite, x, y)

    return grid