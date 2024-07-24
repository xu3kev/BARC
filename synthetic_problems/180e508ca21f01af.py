from common import *

import numpy as np
from typing import *

# concepts:
# scaling, masking, patterns

# description:
# In the input you will see a large patterned square object and a smaller monochromatic object.
# To make the output, first downscale the large patterned square so that it is the same size as the small monochromatic object,
# then use the smaller object as a binary mask to zero out pixels in the scaled-down square.

def main(input_grid):
    # find all the objects in the input grid
    objects = find_connected_components(input_grid, connectivity=8, monochromatic=False)

    # figure out which object is the pattern square and which object is the monochromatic mask
    pattern_square, mask_obj = None, None
    for obj in objects:
        unique_colors = set(obj.flatten())
        if len(unique_colors.difference([Color.BLACK])) > 1:
            pattern_square = obj
        elif len(unique_colors.difference([Color.BLACK])) == 1:
            mask_obj = obj
    
    # get the location and size of the pattern square
    x, y, width, height = bounding_box(pattern_square)
    pattern_sprite = pattern_square[x:x+width, y:y+height]

    # get the location and size of the mask object
    x2, y2, width2, height2 = bounding_box(mask_obj)
    # make sure the mask object is square
    if width2 != height2:
        width2 = height2 = max(width2, height2)
    mask_sprite = mask_obj[x2:x2+width2, y2:y2+height2]

    # calculate the scaling factor
    scale = width // width2
    if scale == 0:
        scale = 1

    # scale down the pattern to fit the mask object
    scaled_pattern = np.zeros((width2, height2), dtype=int)
    for i in range(width2):
        for j in range(height2):
            scaled_pattern[i,j] = pattern_sprite[i * scale, j * scale]
    
    # apply the mask
    output_grid = np.where(mask_sprite != Color.BLACK, scaled_pattern, Color.BLACK)

    return output_grid


def generate_input():
    # decide how big the large patterned square will be
    size = np.random.randint(12, 16)

    # make the large patterned square with random colors
    pattern_square = random_sprite(size, size, density=0.7, symmetry="not_symmetric", color_palette=list(Color.NOT_BLACK))
    
    # make sure the pattern is continuous, if not then try again
    if not is_contiguous(pattern_square, connectivity=8):
        return generate_input()

    # decide how big the small monochromatic mask object will be
    mask_size = np.random.randint(3, 5)

    # make the monochromatic mask object with one random color
    mask_color = np.random.choice(list(Color.NOT_BLACK))
    mask_obj = random_sprite(mask_size, mask_size, density=0.5, symmetry="not_symmetric", color_palette=[mask_color])
    
    # check that mask object is continuous, if not then try again
    if not is_contiguous(mask_obj, connectivity=8):
        return generate_input()

    # make a grid large enough to fit both the patterned square and the monochromatic mask
    n, m = max(size, mask_size + 1) + np.random.randint(2, 5), max(size, mask_size + 1) + np.random.randint(2, 5)
    grid = np.zeros((n, m), dtype=int)

    # put the patterned square on the grid randomly
    x, y = np.random.randint(0, n - size), np.random.randint(0, m - size)
    blit_sprite(grid, pattern_square, x=x, y=y)

    # put the monochromatic mask object on the grid randomly but not touching the patterned square
    x2, y2 = random_free_location_for_sprite(grid, mask_obj)
    # make sure the mask object is not touching the patterned square, if it is then keep looking for a place to put it
    while contact(object1=grid, object2=mask_obj, x2=x2, y2=y2, connectivity=8):
        x2, y2 = random_free_location_for_sprite(grid, mask_obj)
    blit_sprite(grid, mask_obj, x=x2, y=y2)

    return grid