from common import *

import numpy as np
from typing import *

# concepts:
# objects, alignment by color

# description:
# In the input you will see some objects scattered around on a black grid. Each object has a single grey pixel, but everything else is a single other color.
# To make the output, place each object into the output grid such that the grey pixel is in the center of the output.
# Equivalently, move the objects to line up all their grey pixels so they overlap.
# The output grid should be the smallest possible size that contains all the objects (after they have been placed correctly), which for all the inputs here is 3x3.

def main(input_grid):
    # Plan:
    # 1. Extract the objects from the input, convert them into sprites by cropping them
    # 2. Make a big output grid
    # 3. Place each sprite into the output grid such that the grey pixel is in the center of the output
    # 4. Make the output as small as you can to contain all the objects

    # Extract the objects from the input. It is not monochromatic because the grey pixel is different, and they can be connected on the diagonals (connectivity=8)
    objects = find_connected_components(input_grid, monochromatic=False, connectivity=8)

    # Convert the objects into sprites by cropping them
    sprites = [crop(obj, background=Color.BLACK) for obj in objects]

    # Make a big output grid
    output_grid = np.full(input_grid.shape, Color.BLACK)

    # Place each sprite into the output grid such that the grey pixel is in the center of the output
    for sprite in sprites:
        # Find the grey pixel
        grey_pixel_x, grey_pixel_y = np.argwhere(sprite == Color.GREY)[0]

        # Find the center of the output. We want the grey pixel to end up here.
        center_x, center_y = output_grid.shape[0] // 2, output_grid.shape[1] // 2

        # Calculate the offset to ensure the grey pixel ends up in the center of the output
        x, y = center_x - grey_pixel_x, center_y - grey_pixel_y
        
        # Place the sprite into the output grid
        blit_sprite(output_grid, sprite, x, y, background=Color.BLACK)

    # Make the output as small as you can to contain all the objects
    output_grid = crop(output_grid)

    return output_grid


def generate_input():
    # Create a series of 3x3 objects, each of which has a great pixel at the center, and none of which overlap except for the grey pixels
    sprites = []

    # To make sure there is no overlap, we keep track of what pixels are already occupied
    occupied = np.full((3, 3), False)

    n_objects = np.random.randint(2, 4)
    for _ in range(n_objects):
        sprite = np.full((3, 3), Color.BLACK)
        sprite[1, 1] = Color.GREY
        other_color = random.choice([c for c in Color.NOT_BLACK if c != Color.GREY])

        # Randomly pick a subset of valid pixels to color
        # To be valid it has to be unoccupied and not grey (it will be black)
        valid_pixels = np.argwhere(~occupied & (sprite == Color.BLACK))
        if len(valid_pixels) == 0:
            break

        n_pixels = np.random.randint(1, len(valid_pixels) + 1)
        pixels = valid_pixels[np.random.choice(len(valid_pixels), n_pixels, replace=False)]
        for x, y in pixels:
            sprite[x, y] = other_color
            occupied[x, y] = True
        
        sprites.append(sprite)

    # Place the sprites randomly on a medium sized canvas but make sure they don't touch each other
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    grid = np.full((n, m), Color.BLACK)
    for sprite in sprites:
        x, y = random_free_location_for_sprite(grid, sprite, padding=2, padding_connectivity=8)
        blit_sprite(grid, sprite, x, y)

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
