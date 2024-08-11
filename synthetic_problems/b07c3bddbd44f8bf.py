from common import *

import numpy as np
from typing import *

# concepts:
# objects, alignment by color, reflection

# description:
# In the input you will see some objects scattered around on a black grid. Each object has a pixel of some unique color that distinguishes it.
# To make the output, reflect the objects vertically, and place each reflected object such that the unique colored pixel in the reflection overlaps with the unique colored pixel in the original object.
# The output grid should be the smallest possible size that contains all the objects (after they have been placed correctly), which for all the inputs here might be larger than the input but should be appropriately cropped.

def main(input_grid):
    # Plan:
    # 1. Find the objects from the input grid
    # 2. Reflect each object vertically
    # 3. Place the reflected objects in the output grid such that the unique colored pixel of the reflection overlaps with that of the original object
    # 4. Crop the output grid to the smallest size that contains all the aligned objects

    # Step 1: Find the objects from the input grid
    objects = find_connected_components(input_grid, monochromatic=False, connectivity=8)
    sprites = [crop(obj, background=Color.BLACK) for obj in objects]

    # Step 2: Reflect each object vertically
    reflected_sprites = [np.flipud(sprite) for sprite in sprites]

    # Step 3: Create an empty output grid larger than or equal to the input grid
    output_grid = np.full((input_grid.shape[0] * 2, input_grid.shape[1]), Color.BLACK)

    for original_sprite, reflected_sprite in zip(sprites, reflected_sprites):
        # Find the unique colored pixel in the original object
        unique_color = next(color for color in np.unique(original_sprite) if color != Color.BLACK)
        original_pixel_pos = np.argwhere(original_sprite == unique_color)[0]

        # Find the point in the reflected sprite that should align with the original unique colored pixel
        reflected_pixel_pos = np.argwhere(reflected_sprite == unique_color)[0]

        # Offset to place the reflected sprite
        x_offset = original_pixel_pos[0] - reflected_pixel_pos[0]
        y_offset = original_pixel_pos[1] - reflected_pixel_pos[1] + input_grid.shape[0]

        # Place both the original and reflected objects in their aligned positions in the output grid
        blit_sprite(output_grid, original_sprite, 0, y_offset, background=Color.BLACK)
        blit_sprite(output_grid, reflected_sprite, input_grid.shape[0], y_offset, background=Color.BLACK)

    # Step 4: Crop the output grid to the smallest size that contains all the aligned objects
    output_grid = crop(output_grid)

    return output_grid


def generate_input():
    n, m = np.random.randint(10, 20), np.random.randint(10, 20)
    input_grid = np.full((n, m), Color.BLACK)

    n_objects = np.random.randint(2, 5)
    for _ in range(n_objects):
        sprite_size = np.random.randint(3, 5)
        sprite = np.full((sprite_size, sprite_size), Color.BLACK)

        # Create a random object with a unique colored pixel
        unique_color = np.random.choice(list(Color.NOT_BLACK))
        other_color = np.random.choice([c for c in Color.NOT_BLACK if c != unique_color])

        # Place unique colored pixel
        sprite[sprite_size // 2, sprite_size // 2] = unique_color

        # Fill the rest of the object with the other color
        for i in range(sprite_size):
            for j in range(sprite_size):
                if sprite[i, j] != unique_color:
                    sprite[i, j] = other_color

        x, y = random_free_location_for_sprite(input_grid, sprite, padding=2, padding_connectivity=8)
        blit_sprite(input_grid, sprite, x, y)

    return input_grid