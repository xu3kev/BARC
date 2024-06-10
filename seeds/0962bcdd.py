from common import *

import numpy as np
from typing import *

# concepts:
# pixel manipulation, growing

# description:
# In the input you will see some number of colored crosses, each of which is 3 pixels tall, 3 pixels wide, and has a single pixel in the center of the cross that is a different color.
# Make the output by growing the cross by 1 pixel north/south/east/west, and growing the center pixel by 2 pixels along each of the 4 diagonals.

def main(input_grid):

    # extract the 3x3 crosses
    crosses = find_connected_components(input_grid, background=Color.BLACK, monochromatic=False)

    output_grid = input_grid.copy()

    for cross in crosses:
        # find the center
        x, y, w, h = bounding_box(cross)
        center_x, center_y = x + w//2, y + h//2

        # extract the relevant colors
        center_color = cross[center_x, center_y]
        cross_color = cross[cross != Color.BLACK][0]

        # grow the cross
        for i in range(x-1, x+w+1):
            for j in range(y-1, y+h+1):
                if i == center_x or j == center_y:
                    output_grid[i, j] = cross_color
                if i - center_x == j - center_y or i - center_x == center_y - j:
                    output_grid[i, j] = center_color

    return output_grid



def generate_input():
    input_grid = np.zeros((20, 20), dtype=int)

    # create 2 crosses
    for cross_number in range(2):
        # create a separate sprite
        cross = np.zeros((3, 3), dtype=int)
        cross_color, center_color = random.sample(list(Color.NOT_BLACK), 2)
        cross[1, :] = cross_color
        cross[:, 1] = cross_color
        cross[1, 1] = center_color

        # find a free place on the grid
        x, y = random_free_location_for_object(input_grid, cross)

        # blit the cross to the canvas
        blit(input_grid, cross, x, y)

    return input_grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)