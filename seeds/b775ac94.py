from common import *

import numpy as np
from typing import *

# concepts:
# symmetry, mirror

# description:
# In the input you will see big objects with a primary color and some single pixels of different colors attached to it.
# To make the output, mirror the primary colored part of each object over the differently colored pixels attached to it, changing the primary color to match the other color.

def main(input_grid):
    # Plan
    # 1. Parse the input into primary regions and their associated single pixel indicators
    # 2. For each primary region and each attached indicator pixel, change color and mirror.

    # 1. Input parsing
    background = Color.BLACK
    objects = find_connected_components(grid=input_grid, connectivity=8, monochromatic=True, background=background)
    indicator_pixels = [ obj for obj in objects if np.sum(obj != background) == 1 ]
    primary_objects = [ obj for obj in objects if np.sum(obj != background) > 1 ]

    # 2. Output generation

    # Copy the input because we draw on top of it
    output_grid = input_grid.copy()

    # loop over primary objects and every pixel that they are in contact with
    for primary_object in primary_objects:
        for indicator_pixel in indicator_pixels:
            if not contact(object1=primary_object, object2=indicator_pixel, background=background, connectivity=8): continue

            # Recolor
            indicator_color = object_colors(indicator_pixel, background=background)[0]
            recolored_object = np.copy(primary_object)
            recolored_object[primary_object != background] = indicator_color

            # Build the mirroring object
            indicator_x, indicator_y = object_position(indicator_pixel, background=background, anchor="upper left")
            primary_x1, primary_y1 = object_position(primary_object, background=background, anchor="upper left")
            primary_x2, primary_y2 = object_position(primary_object, background=background, anchor="lower right")
            # If it's in the corners, we mirror diagonally (over both x and y)
            # If it's on the left/right side, we mirror horizontally
            # If it's on the top/bottom side, we mirror vertically
            mirror_x, mirror_y = None, None
            if indicator_x == primary_x1-1: mirror_x = primary_x1-0.5
            if indicator_x == primary_x2+1: mirror_x = primary_x2+0.5
            if indicator_y == primary_y1-1: mirror_y = primary_y1-0.5
            if indicator_y == primary_y2+1: mirror_y = primary_y2+0.5
            symmetry = MirrorSymmetry(mirror_x=mirror_x, mirror_y=mirror_y)

            # Mirror the primary object over the indicator pixel
            for x, y in np.argwhere(primary_object != background):
                x2, y2 = symmetry.apply(x, y)
                if 0 <= x2 < output_grid.shape[0] and 0 <= y2 < output_grid.shape[1]:
                    output_grid[x2, y2] = recolored_object[x, y]

    return output_grid

def generate_input():
    # Create monochromatic objects and then attach differently colored indicator pixels at one of their corners
    width, height = np.random.randint(15, 30), np.random.randint(15, 30)
    grid = np.zeros((width, height), dtype=int)

    num_objects = np.random.randint(1, 4)
    for _ in range(num_objects):
        # we'll attach indicators to the upper left and then randomly rotate the sprite before putting it on the canvas
        # at most three indicators, so we'll choose a primary color and then choose the indicator colors from the rest5
        max_indicators = 3
        num_indicators = np.random.randint(1, max_indicators+1)
        primary_color, *indicator_colors = np.random.choice(Color.NOT_BLACK, size=num_indicators+1, replace=False)

        # create sprite with indicators attached to it in the upper left. it must be contiguous, so we loop until we find one that is
        while True:
            sprite = random_sprite([3,4,5,6], [3,4,5,6], color_palette=[primary_color], symmetry="not_symmetric")
            # Clear place for indicators in the upper left
            sprite[:1, :] = Color.BLACK
            sprite[:, :1] = Color.BLACK
            # three indicator locations in the upper left corner
            indicator_locations = [(0, 0), (0, 1), (1, 0)]
            random.shuffle(indicator_locations)
            for color, (x, y) in zip(indicator_colors, indicator_locations):
                sprite[x, y] = color
            # make sure that the upper left corner is connected to the rest of the sprite
            if sprite[1, 1] == primary_color: break
        
        # randomly rotate to get variety of orientations
        sprite = np.rot90(sprite, k=np.random.randint(4))
        
        # randomly place the sprite on the grid
        x, y = random_free_location_for_sprite(grid, sprite, padding=max(sprite.shape), padding_connectivity=8)
        blit_sprite(grid, sprite, x, y)

    return grid

            



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
