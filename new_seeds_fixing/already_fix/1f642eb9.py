from common import *

import numpy as np
from typing import *

# concepts:
# alignment, copy to object border

# description:
# In the input you will see a teal object on a black background, and several colored pixels on the border of canvas.
# To make the output grid, you should copy the colored pixels horizontally/vertically so that they are just barely overlapping/colliding with the teal object.

def main(input_grid):
    # Plan:
    # 1. Detect the teal object
    # 2. Detect the colored pixels on the border
    # 3. Slide the colored pixels in the 4 cardinal directions until we find how to make them overlapping with the teal object

    output_grid = np.copy(input_grid)

    # Detects the rectangle in the input grid that is TEAL
    teal_objects = detect_objects(grid=input_grid, colors=[Color.TEAL], monochromatic=True, connectivity=4)
    
    # There should only be one rectangle of the color TEAL has been detected in the grid.
    assert len(teal_objects) == 1
    teal_object = teal_objects[0]

    # colored pixels are NOT black and NOT TEAL.
    colors_except_teal = [c for c in Color.NOT_BLACK if c != Color.TEAL]
    
    # Detects all other colored pixels in the grid 
    pixels = detect_objects(grid=input_grid,
                            # Exclude teal from the search
                            colors=colors_except_teal, 
                            # only consider single pixels
                            allowed_dimensions=[(1,1)], 
                            monochromatic=True, connectivity=4)

    # Copy the colored pixels to the teal object by moving them either vertically or horizontally.
    for pixel in pixels:
        # consider translating the pixel in the 4 cardinal directions, and consider translating as far as possible
        possible_displacements = [ (slide_distance*dx, slide_distance*dy)
                                   # We could slide as far as the maximum grid extent
                                   for slide_distance in range(max(input_grid.shape))
                                   # (dx, dy) ranges over 4 cardinal directions
                                   for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)] ]
        for dx, dy in possible_displacements:
            # check if the objects are colliding/overlapping after translating
            translated_pixel = translate(pixel, dx, dy, background=Color.BLACK)
            if collision(object1=teal_object, object2=translated_pixel):
                # put the red object where it belongs
                blit_object(output_grid, translated_pixel, background=Color.BLACK)
                break
    
    return output_grid


def generate_input():
    # Initialize a 10x10 grid representing a black background.
    n = m = 10
    grid = np.zeros((n, m), dtype=int)
    
    # Randomly determine the width and height of the TEAL rectangle between 2 and 5.
    width, height = np.random.randint(2, 6), np.random.randint(2, 6)
    teal_sprite = np.full((width, height), Color.TEAL)

    # Find a free location for this sprite and blit it to the grid
    x, y = random_free_location_for_sprite(grid, teal_sprite, background=Color.BLACK, padding=1, border_size=1)
    blit_sprite(grid, teal_sprite, x, y, background=Color.BLACK)

    # list to hold the available positions, which are all on the border of the canvas
    border_locations = [ (0, y) for y in range(n) ] + [ (m-1, y) for y in range(n) ] + [ (x, 0) for x in range(1, m-1) ] + [ (x, n-1) for x in range(1, m-1) ]
    
    # Put a random number of colored pixels on the border of the canvas
    for _ in range(np.random.randint(3, 8)):
        # Pick a random location on the border
        x, y = random.choice(border_locations)
        # Pick a random color that is not black or teal
        color = random.choice([c for c in Color.NOT_BLACK if c != Color.TEAL])

        grid[x, y] = color
    
    return grid 

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)