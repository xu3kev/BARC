from common import *

import numpy as np
from typing import *

# concepts:
# objects, colors, alignment by color

# description:
# In the input grid, you will see several colored objects scattered around with a black background.
# Each object has a single pink pixel, and all other pixels in the object are of a single color.
# To make the output, align all these objects such that the pink pixels overlap.
# The output grid should be the smallest possible size that contains all the objects after aligning them.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Plan:
    # 1. Extract objects from input grid.
    # 2. Convert each object to a sprite by cropping it.
    # 3. Create a minimal size output grid.
    # 4. Align all pink pixels to overlap center.
    
    # 1. Extract objects
    objects = find_connected_components(input_grid, background=Color.BLACK, connectivity=8, monochromatic=False)

    # 2. Convert objects to sprites
    sprites = [crop(obj, background=Color.BLACK) for obj in objects]
    
    # Determine the minimal grid size to contain all sprites aligning pink pixels
    max_sprite_height = max(s.shape[0] for s in sprites)
    max_sprite_width = max(s.shape[1] for s in sprites)
    output_grid_size = (max_sprite_height, max_sprite_width)
    
    # Create a minimal output grid
    output_grid = np.full(output_grid_size, Color.BLACK)

    # 4. Align objects at the center pink pixel
    center_x, center_y = output_grid_size[0] // 2, output_grid_size[1] // 2

    for sprite in sprites:
        pink_pixel_x, pink_pixel_y = np.argwhere(sprite == Color.PINK)[0]
        x, y = center_x - pink_pixel_x, center_y - pink_pixel_y
        blit_sprite(output_grid, sprite, x, y, background=Color.BLACK)

    return output_grid

def generate_input() -> np.ndarray:
    grid_size = (np.random.randint(10, 20), np.random.randint(10, 20))
    input_grid = np.full(grid_size, Color.BLACK)

    num_objects = np.random.randint(2, 5)
    colors = list(Color.NOT_BLACK)

    for _ in range(num_objects):
        color = np.random.choice(colors)
        colors.remove(color)

        obj_size = np.random.randint(3, 6)
        sprite = random_sprite(obj_size, obj_size, density=0.4, color_palette=[color, Color.PINK], connectivity=8)

        # Ensure there's exactly one pink pixel
        pink_pixels = np.argwhere(sprite == Color.PINK)
        if len(pink_pixels) > 1:
            for x, y in pink_pixels[1:]:
                sprite[x, y] = color

        x, y = random_free_location_for_sprite(input_grid, sprite, padding=2, padding_connectivity=8)
        blit_sprite(input_grid, sprite, x, y)

    return input_grid