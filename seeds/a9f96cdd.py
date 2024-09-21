from common import *

import numpy as np
from typing import *

# concepts:
# constant pattern, diagonal corners

# description:
# In the input you will see one red pixel
# To make the output grid, you should 
# 1. draw a pattern with four different colors centered at the red pixel at its diagonal corners:
#    green in the upper left, pink in the upper right, teal in the lower left, and yellow in the lower right.
# 2. remove the red pixel (equivalently start with a blank canvas and draw the pattern at the red pixel location)

def main(input_grid):
    # Find the red single pixel object
    red_pixel_objects = detect_objects(grid=input_grid, colors=[Color.RED], allowed_dimensions=[(1, 1)], monochromatic=True, connectivity=4)
    assert len(red_pixel_objects) == 1
    red_pixel_object = red_pixel_objects[0]

    # Find out the position of the red pixel
    red_x, red_y = object_position(red_pixel_object, background=Color.BLACK, anchor="upper left")

    # Construct the specific pattern that is going to be drawn where the red pixel was
    pattern = np.array([[Color.GREEN, Color.BLACK, Color.PINK], 
                        [Color.BLACK, Color.BLACK, Color.BLACK],
                        [Color.TEAL, Color.BLACK, Color.ORANGE]]).transpose()
    
    # Because sprites are anchored by the upper left corner, we are going to need to calculate where the pattern's upper left corner should be
    pattern_width, pattern_height = pattern.shape
    pattern_x, pattern_y = red_x - pattern_width//2, red_y - pattern_height//2

    # The output grid is the same size of input grid
    # start with a blank canvas and then lit the pattern
    output_grid = np.full(input_grid.shape, Color.BLACK)
    output_grid = blit_sprite(grid=output_grid, x=pattern_x, y=pattern_y, sprite=pattern, background=Color.BLACK)

    return output_grid
    
def generate_input():
    # Generate the background grid with size of n x m.
    n, m = 5, 3
    grid = np.zeros((n, m), dtype=int)

    # Randomly select the position of the red pixel and draw it.
    x, y = np.random.randint(0, n - 1), np.random.randint(0, m - 1)
    grid[x, y] = Color.RED
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)