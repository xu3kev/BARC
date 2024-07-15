from common import *

import numpy as np
from typing import *

# concepts:
# objects, reflection, symmetry, alignment by color

# description:
# In the input grid, you will see several objects each containing a single grey pixel and various other colors.
# The goal is to align all objects symmetrically around the center of the grid using reflection. Specifically, the object that contains the grey pixel closest to the center remains in place,
# while all other objects should be reflected either vertically or horizontally such that their grey pixel aligns with the center grey pixel.
# The resulting output grid will be the smallest bounding box containing all the transformed objects.

def main(input_grid):
    # Extract the objects from the input grid
    objects = find_connected_components(input_grid, monochromatic=False, connectivity=8)
    
    # Crop the objects to get the individual sprites
    sprites = [crop(obj, background=Color.BLACK) for obj in objects]

    # Create a new grid with the same shape as input for placing the transformed sprites
    output_grid = np.full(input_grid.shape, Color.BLACK)

    # Find the center of the grid
    center_x, center_y = input_grid.shape[0] // 2, input_grid.shape[1] // 2
    
    # Source sprite to align to the center
    center_sprite = None
    
    for sprite in sprites:
        grey_pixel_pos = np.argwhere(sprite == Color.GREY)
        if len(grey_pixel_pos) == 0:
            continue
        grey_pixel_x, grey_pixel_y = grey_pixel_pos[0]
        
        # Find the sprite closest to the center
        sprite_center_x = grey_pixel_x + (sprite.shape[0] // 2)
        sprite_center_y = grey_pixel_y + (sprite.shape[1] // 2)
        
        if center_sprite is None or abs(sprite_center_x - center_x) + abs(sprite_center_y - center_y) < abs(center_sprite[0] - center_x) + abs(center_sprite[1] - center_y):
            center_sprite = (grey_pixel_x, grey_pixel_y, sprite)
    
    # Place the center sprite in the center of the output grid
    grey_pixel_x, grey_pixel_y, sprite = center_sprite
    blit_sprite(output_grid, sprite, center_x - grey_pixel_x, center_y - grey_pixel_y, background=Color.BLACK)
    
    # Reflect and align other objects
    for sprite in sprites:
        if np.array_equal(sprite, center_sprite[2]):
            continue
        
        grey_pixel_pos = np.argwhere(sprite == Color.GREY)
        if len(grey_pixel_pos) == 0:
            continue
        grey_pixel_x, grey_pixel_y = grey_pixel_pos[0]

        # Reflect the sprite horizontally or vertically based on alignment to the center sprite
        if abs(grey_pixel_x - center_x) >= abs(grey_pixel_y - center_y):
            # Vertical reflection
            reflected_sprite = np.flipud(sprite)
            blit_sprite(output_grid, reflected_sprite, center_x - grey_pixel_x, center_y - grey_pixel_y, background=Color.BLACK)
        else:
            # Horizontal reflection
            reflected_sprite = np.fliplr(sprite)
            blit_sprite(output_grid, reflected_sprite, center_x - grey_pixel_x, center_y - grey_pixel_y, background=Color.BLACK)

    # Crop the output grid to the smallest bounding box containing all sprites
    output_grid = crop(output_grid)

    return output_grid


def generate_input():
    # Create a series of 3x3 objects, each of which has a grey pixel at a random position
    n_objects = np.random.randint(3, 5)
    sprites = []

    for _ in range(n_objects):
        sprite = np.full((3, 3), Color.BLACK)

        grey_pixel_x, grey_pixel_y = np.random.randint(0, 3), np.random.randint(0, 3)
        sprite[grey_pixel_x, grey_pixel_y] = Color.GREY
        other_color = np.random.choice([color for color in Color.NOT_BLACK if color != Color.GREY])
        
        for x in range(3):
            for y in range(3):
                if sprite[x, y] == Color.BLACK:
                    sprite[x, y] = np.random.choice([Color.BLACK, other_color], p=[0.6, 0.4])
        
        sprites.append(sprite)

    # Place sprites randomly on the grid, ensuring no overlap
    grid_size = np.random.randint(10, 15), np.random.randint(10, 15)
    grid = np.full(grid_size, Color.BLACK)

    for sprite in sprites:
        x, y = random_free_location_for_sprite(grid, sprite, padding=1, padding_connectivity=8)
        blit_sprite(grid, sprite, x, y)

    return grid