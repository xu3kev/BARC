from common import *

import numpy as np
from typing import *

# concepts:
# symmetries, objects

# description:
# In the input you will see one or two medium-sized multicolor objects, and some multicolor pixels sprinkled around in one or two clusters
# To make the output, take each of the medium-sized object and move it so that it perfectly covers some of the pixels sprinkled around, matching colors wherever they overlap.
# You can rotate and flip the objects in order to make them fit the pixels, but they have to match colors wherever they overlap.

def main(input_grid):
    # Plan:
    # 1. Break the input into 1-2 big object(s) and a mask containing the remaining pixels
    # 2. For each object, create rotations and flips of it
    # 3. For each object, find the best way to place one of its rotations/flips so that it covers the most number of the pixels (remember the pixel has to match object color)

    # Extract the objects from the input and categorize them into objects and pixels
    # Objects can be multicolored
    connected_components = find_connected_components(input_grid, monochromatic=False)
    objects = [ cc for cc in connected_components if np.count_nonzero(cc != Color.BLACK) > 4 ]
    pixels = [ cc for cc in connected_components if np.count_nonzero(cc != Color.BLACK) <= 4 ]

    # Make the pixel mask, which shows where the pixels are. These guide the placement of objects.
    pixel_mask = np.full(input_grid.shape, Color.BLACK)
    for pixel_object in pixels:
        blit_object(pixel_mask, pixel_object, background=Color.BLACK)
    
    output_grid = np.full(input_grid.shape, Color.BLACK)
    
    # For each object, find the best way to place it so that it covers the most number of the pixels
    for obj in objects:
        # The object can be rotated and flipped to match the pixels
        # First, convert it to a sprite before transforming, because these operations are independent of position
        sprite = crop(obj)
        sprite_variations = [sprite, np.rot90(sprite), np.rot90(sprite, 2), np.rot90(sprite, 3), np.flipud(sprite), np.fliplr(sprite), np.flipud(np.rot90(sprite)), np.fliplr(np.rot90(sprite))]

        # We are going to optimize the position and variation, so we need to keep track of the best placement so far
        best_output, best_pixels_covered = None, 0
        for x, y, sprite_variation in [(x, y, variant) for x in range(input_grid.shape[0]) for y in range(input_grid.shape[1]) for variant in sprite_variations]:
            test_grid = np.copy(output_grid)
            blit_sprite(test_grid, sprite_variation, x, y, background=Color.BLACK)
            # Check if there was any color mismatch: A colored pixel in the mask which is different from what we just made
            # If there is a mismatch, we can't place the object here
            if np.any((pixel_mask != Color.BLACK) & (test_grid != Color.BLACK) & (pixel_mask != test_grid)):
                continue
            num_covered_pixels = np.count_nonzero((pixel_mask != Color.BLACK) & (test_grid != Color.BLACK))
            if num_covered_pixels > best_pixels_covered:
                best_output, best_pixels_covered = test_grid, num_covered_pixels
        output_grid = best_output

    return output_grid


def generate_input():
    # to make the input, we make random objects
    # we need to make sure that the objects can match with the "sprinkled" pixels, so we make the pixels by placing some objects and then removing some parts of them

    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.full((n, m), Color.BLACK)

    num_objects = np.random.randint(1, 3)
    sprites = [ random_sprite(np.random.randint(3, 6), np.random.randint(3, 6), color_palette=Color.NOT_BLACK, density=0.5)
                for _ in range(num_objects) ]
    sprite_variations = [ [sprite, np.rot90(sprite), np.rot90(sprite, 2), np.rot90(sprite, 3), np.flipud(sprite), np.fliplr(sprite), np.flipud(np.rot90(sprite)), np.fliplr(np.rot90(sprite))]
                          for sprite in sprites ]
    # Pick a variation for each sprite
    sprite_variations = [ random.choice(variations) for variations in sprite_variations ]
    
    # Remove parts of the sprite to create the "sprinkled" pixels
    # We remove enough of the sprite so that there are only 3 pixels remaining
    # We do this to the variation, which is what is going to be put on the canvas to be matched with
    occluded_sprites = []
    for sprite in sprite_variations:
        occluded_sprite = np.copy(sprite)
        could_be_removed = np.argwhere(occluded_sprite != Color.BLACK)
        np.random.shuffle(could_be_removed)
        for i in range(len(could_be_removed) - 3):
            x, y = could_be_removed[i]
            occluded_sprite[x, y] = Color.BLACK

        occluded_sprites.append(occluded_sprite)

    # place everything on the canvas but make sure that nothing overlaps, so they all have their own free location with a little bit of padding
    for sprite in sprites + occluded_sprites:
        x, y = random_free_location_for_sprite(grid, sprite, padding=2, border_size=2)
        blit_sprite(grid, sprite, x, y)
    
    return grid     

    

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
