from common import *
import numpy as np
from typing import *

# concepts:
# objects, color, growing, pixel manipulation

# description:
# In the input, you will see several colored squares of different sizes with their centers filled with a different color.
# To make the output, grow each square by adding a layer of their edge color around each square while retaining their center color as it is.

def main(input_grid):
    output_grid = np.copy(input_grid)

    # extract the squares
    squares = find_connected_components(input_grid, background=Color.BLACK, monochromatic=False)

    for square in squares:
        # find the bounding box of the square
        x, y, w, h = bounding_box(square)
        center_x, center_y = x + w // 2, y + h // 2

        # extract the relevant colors
        center_color = square[center_x, center_y]
        edge_color = square[square != center_color][0]

        # grow the square by 1 pixel layer around the edges
        for i in range(x - 1, x + w + 1):
            for j in range(y - 1, y + h + 1):
                # skip if out of bounds
                if i < 0 or j < 0 or i >= input_grid.shape[0] or j >= input_grid.shape[1]:
                    continue

                # grow the square's edge
                if (i == x - 1 or i == x + w) or (j == y - 1 or j == y + h):
                    output_grid[i, j] = edge_color

                # retain the center color unchanged
                if (i == center_x and j == center_y):
                    output_grid[i, j] = center_color

    return output_grid

def generate_input():
    n = m = 20
    input_grid = np.zeros((n, m), dtype=int)

    # create 2-5 squares of random sizes
    num_squares = np.random.randint(2, 6)
    for _ in range(num_squares):
        side_length = np.random.choice([3, 5, 7])
        square = np.zeros((side_length, side_length), dtype=int)
        
        edge_color, center_color = random.sample(list(Color.NOT_BLACK), 2)
        square[:, :] = edge_color
        middle = side_length // 2
        square[middle, middle] = center_color

        # find a free place on the grid
        x, y = random_free_location_for_sprite(input_grid, square, border_size=1, padding=0)

        # blit the square to the canvas
        blit_sprite(input_grid, square, x, y)

    return input_grid