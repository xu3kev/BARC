from common import *

import numpy as np
from typing import *

# concepts:
# color, growing, objects, pixel manipulation

# description:
# In the input you will see some number of colored diamonds, each of which is 5 pixels tall, 5 pixels wide, and has a single pixel in the center of the diamond that is a different color.
# Make the output by growing the diamond by 1 pixel layer outward, and change the outermost pixels to match the color of the center pixel.

def main(input_grid):
    # extract the diamonds
    diamonds = find_connected_components(input_grid, background=Color.BLACK, monochromatic=False)

    output_grid = np.copy(input_grid)

    for diamond in diamonds:
        # find the center
        x, y, w, h = bounding_box(diamond)
        center_x, center_y = x + w // 2, y + h // 2

        # extract the relevant colors
        center_color = diamond[center_x, center_y]
        diamond_color = diamond[diamond != Color.BLACK][0]

        # grow the diamond layer
        for dx in range(-(w // 2 + 1), w // 2 + 2):
            for dy in range(-(h // 2 + 1), h // 2 + 2):
                output_x, output_y = center_x + dx, center_y + dy
                # skip if out of bounds
                if output_x < 0 or output_y < 0 or output_x >= input_grid.shape[0] or output_y >= input_grid.shape[1]:
                    continue
                
                # grow the diamond in a layered fashion
                distance_from_center = abs(dx) + abs(dy)
                if distance_from_center == w // 2 + 1:  # Outermost layer
                    output_grid[output_x, output_y] = center_color
                elif distance_from_center <= w // 2:  # Existing diamond and expanded part
                    output_grid[output_x, output_y] = diamond_color

    return output_grid

def generate_input():
    input_grid = np.zeros((20, 20), dtype=int)

    # create 2 diamonds
    for diamond_number in range(2):
        # create a separate sprite
        diamond = np.zeros((5, 5), dtype=int)
        diamond_color, center_color = random.sample(list(Color.NOT_BLACK), 2)

        center = 2
        diamond[center, :] = diamond_color
        diamond[:, center] = diamond_color
        for i in range(1, 5, 2):
            diamond[center - i // 2, center - i // 2] = diamond_color
            diamond[center + i // 2, center + i // 2] = diamond_color
            diamond[center - i // 2, center + i // 2] = diamond_color
            diamond[center + i // 2, center - i // 2] = diamond_color
        diamond[center, center] = center_color

        # find a free place on the grid
        x, y = random_free_location_for_sprite(input_grid, diamond, padding=1, padding_connectivity=8)

        # blit the diamond to the canvas
        blit_sprite(input_grid, diamond, x, y)

    return input_grid