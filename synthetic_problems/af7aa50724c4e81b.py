from common import *

import numpy as np
from typing import *

# concepts:
# objects, color guide, masking, scaling, proximity

# description:
# In the input, you will see two objects: a large monochromatic object (the "mask") and a smaller multi-colored object (the "guide").
# To make the output:
# 1. Scale down the mask to be the same size as the guide.
# 2. For each pixel in the scaled-down mask:
#    a. If the pixel is not black, find the closest non-black pixel in the guide.
#    b. Copy the color of that closest pixel from the guide to the output.
# 3. The output should be the same size as the guide, with black where the mask was black.

def main(input_grid):
    # Find all objects in the input grid
    objects = find_connected_components(input_grid, connectivity=8, monochromatic=False)

    # Identify the mask (monochromatic) and the guide (multi-colored)
    mask = guide = None
    for obj in objects:
        if len(set(obj.flatten()) - {Color.BLACK}) == 1:
            mask = obj
        else:
            guide = obj
    
    # Get the bounding boxes
    mx, my, mw, mh = bounding_box(mask)
    gx, gy, gw, gh = bounding_box(guide)

    # Extract the sprites
    mask_sprite = mask[mx:mx+mw, my:my+mh]
    guide_sprite = guide[gx:gx+gw, gy:gy+gh]

    # Scale down the mask to match the guide size
    scale_x, scale_y = mw // gw, mh // gh
    scaled_mask = np.zeros_like(guide_sprite)
    for i in range(gw):
        for j in range(gh):
            scaled_mask[i,j] = mask_sprite[i * scale_x, j * scale_y]

    # Create the output grid
    output_grid = np.full_like(guide_sprite, Color.BLACK)

    # For each non-black pixel in the scaled mask, find the closest non-black pixel in the guide
    for i in range(gw):
        for j in range(gh):
            if scaled_mask[i,j] != Color.BLACK:
                closest_color = min(
                    ((x, y) for x in range(gw) for y in range(gh) if guide_sprite[x,y] != Color.BLACK),
                    key=lambda p: abs(p[0] - i) + abs(p[1] - j)
                )
                output_grid[i,j] = guide_sprite[closest_color]

    return output_grid

def generate_input():
    # Decide the size of the guide
    guide_size = np.random.randint(4, 7)

    # Create the guide with multiple colors
    guide = random_sprite(guide_size, guide_size, density=0.7, symmetry="not_symmetric", color_palette=Color.NOT_BLACK)

    # Ensure the guide has more than one color
    if len(set(guide.flatten()) - {Color.BLACK}) <= 1:
        return generate_input()

    # Create the mask with a single color
    mask_color = np.random.choice(list(Color.NOT_BLACK))
    mask_size = guide_size * np.random.randint(3, 6)
    mask = random_sprite(mask_size, mask_size, density=0.6, symmetry="not_symmetric", color_palette=[mask_color], connectivity=8)

    # Ensure the mask is contiguous
    if not is_contiguous(mask, connectivity=8):
        return generate_input()

    # Create the input grid
    grid_size = mask_size + guide_size + np.random.randint(3, 6)
    grid = np.zeros((grid_size, grid_size), dtype=int)

    # Place the mask
    mx, my = np.random.randint(0, grid_size - mask_size), np.random.randint(0, grid_size - mask_size)
    blit_sprite(grid, mask, x=mx, y=my)

    # Place the guide, ensuring it doesn't touch the mask
    gx, gy = random_free_location_for_sprite(grid, guide, padding=1)
    while contact(object1=grid, object2=guide, x2=gx, y2=gy, connectivity=8):
        gx, gy = random_free_location_for_sprite(grid, guide, padding=1)
    blit_sprite(grid, guide, x=gx, y=gy)

    return grid