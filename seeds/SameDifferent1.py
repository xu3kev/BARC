from common import *

import numpy as np
from typing import *

# concepts:
# same/different

# description:
# In the input you will see some monochromatic objects
# To make the output, keep only those objects which have the same shape as another object (but the color might be different). Equivalently delete all objects which are unique in shape (independent of color).

def main(input_grid):
    # Plan:
    # 1. Extract the objects
    # 2. Compute the mask of the sprite for each object
    # 3. Check to see which masks have another mask which has the same shape
    # 4. Keep only those objects: Blit them to the output

    # Extract the objects
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=8, monochromatic=True)

    # Compute sprites (by cropping), then compute masks
    sprites = [ crop(obj, background=Color.BLACK) for obj in objects]
    masks = [ sprite != Color.BLACK for sprite in sprites ]

    # Compute if there is another thing with the same mask, and if so, put it in the output
    output_grid = np.full_like(input_grid, Color.BLACK)
    for object_index in range(len(objects)):
        obj = objects[object_index]
        sprite = sprites[object_index]
        mask = masks[object_index]

        # Check if the mask is the same as any of the other object masks
        other_object_masks = masks[:object_index] + masks[object_index+1:]
        if any(np.array_equal(mask, other_mask) for other_mask in other_object_masks):
            x, y = object_position(obj, anchor="upper left")
            blit_sprite(output_grid, sprite, x, y)

    return output_grid

def generate_input():
    # Make some sprites
    # Some of those sprites are going to occur more than once in the output (but with different color), hence they are going to have a same shape partner
    # Some of those sprites are going to occur only once in the output, are unique in shape
    n_sprites = np.random.randint(2, 4)
    possible_sprite_dimensions = [1,2,3,4]
    sprites = [ random_sprite(possible_sprite_dimensions, possible_sprite_dimensions, color_palette=[random.choice(Color.NOT_BLACK)])
               for _ in range(n_sprites) ]
    
    width, height = random.choice(range(7, 20)), random.choice(range(7, 20))
    grid = np.full((width, height), Color.BLACK)

    # Randomly pick a subset of the sprites to have a same-shape duplicate
    n_duplicate_sprites = np.random.randint(1, n_sprites)
    duplicated_sprites = random.sample(sprites, n_duplicate_sprites)

    for sprite in sprites:
        # first we put down the original sprite
        x, y = random_free_location_for_sprite(grid, sprite, background=Color.BLACK, border_size=0, padding=0)
        blit_sprite(grid, sprite, x, y)

        # Check if it is one that we should duplicate
        if any( sprite is to_duplicate for to_duplicate in duplicated_sprites ):
            # Create a duplicate with a different color
            duplicate_sprite = sprite.copy()
            # Random color
            duplicate_sprite[duplicate_sprite != Color.BLACK] = random.choice(Color.NOT_BLACK)
            # Random new location
            x, y = random_free_location_for_sprite(grid, duplicate_sprite, background=Color.BLACK, border_size=0, padding=0)
            blit_sprite(grid, duplicate_sprite, x, y)
    
    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
