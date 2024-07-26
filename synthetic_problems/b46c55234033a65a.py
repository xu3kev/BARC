from common import *

import numpy as np
from typing import *

# concepts:
# objects, pixel manipulation, alignment by color, resizing

# description:
# In the input grid, you will see multiple non-black objects of various colors scattered around on a black background.
# Each object will contain exactly one pixel of a unique color (which is not black or the color of the object).
# The goal is to extract the dimensions of each object from the input grid, enlarge each one of them to double its original size, 
# and align them vertically in the output grid based on the unique colored pixel, such that the unique colored pixel lies directly on top of each other vertically.

def main(input_grid):
    # Extract the objects from the input grid
    objects = find_connected_components(input_grid, monochromatic=False, connectivity=8)

    # Collect sprites and their unique colored pixels
    sprites = []
    unique_colors = []
    for obj in objects:
        sprite = crop(obj, background=Color.BLACK)
        unique_color_pixel = [color for color in set(sprite.flatten()) if color != Color.BLACK and np.count_nonzero(sprite == color) == 1]
        
        if unique_color_pixel:
            unique_colors.append(unique_color_pixel[0])
            sprites.append(sprite)
    
    # Enlarge each sprite to double its original size
    enlarged_sprites = []
    for sprite in sprites:
        enlarged_sprite = np.kron(sprite, np.ones((2, 2), dtype=int))
        enlarged_sprites.append(enlarged_sprite)
    
    # Create the output grid
    max_width = max(sprite.shape[1] for sprite in enlarged_sprites)
    total_height = sum(sprite.shape[0] for sprite in enlarged_sprites)
    output_grid = np.full((total_height, max_width), Color.BLACK)

    # Place enlarged sprites vertically centered based on their unique color pixel
    current_y = 0
    for sprite, unique_color in zip(enlarged_sprites, unique_colors):
        # Find the position of the unique colored pixel in the enlarged sprite
        unique_pixel_pos = np.argwhere(sprite == unique_color)[0]
        center_x = (max_width // 2) - unique_pixel_pos[1]

        # Blit the sprite ensuring unique colored pixels are vertically aligned
        blit_sprite(output_grid, sprite, current_y, center_x, background=Color.BLACK)
        current_y += sprite.shape[0]
        
    return output_grid

def generate_input():
    # Create a medium-sized input grid
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.full((n, m), Color.BLACK)

    # Generate a few random colored objects with one unique colored pixel each
    num_objects = np.random.randint(2, 5)
    for _ in range(num_objects):
        object_color = np.random.choice(list(Color.NOT_BLACK))
        unique_color = np.random.choice([c for c in list(Color.NOT_BLACK) if c != object_color])
        
        # Generate a random sprite of size between 2 and 4 with the object color and adding the unique color pixel
        sprite_size = np.random.randint(2, 5)
        sprite = random_sprite(sprite_size, sprite_size, color_palette=[object_color])

        # Find a random position in the sprite to place the unique color pixel
        rand_x, rand_y = np.random.randint(0, sprite_size), np.random.randint(0, sprite_size)
        sprite[rand_x, rand_y] = unique_color
        
        # Place the sprite randomly in the grid, ensuring they do not overlap
        x, y = random_free_location_for_sprite(grid, sprite, padding=1, padding_connectivity=8)
        blit_sprite(grid, sprite, x, y)
        
    return grid