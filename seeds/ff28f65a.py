from common import *

import numpy as np
from typing import *

# concepts:
# counting, object detection, alternating pattern

# description:
# In the input you will see several 2 x 2 red squares on the grid.
# To make the output grid, you should count the number of red squares
# Then place the same number of 1 x 1 blue squares on the output grid following this pattern in the output:
# First fill the top row, then the next row, but skip every other column. Begin the first/third/fifth/etc row in the first column, but begin the second/forth/etc row in the second column.

def main(input_grid):
    # Detect all the 2 x 2 red squares on the grid.
    red_square = detect_objects(grid=input_grid, colors=[Color.RED], monochromatic=True, connectivity=4)

    # Count the number of 2 x 2 red squares.
    num_red_square = len(red_square)

    # Output grid is always 3 x 3.
    output_grid = np.zeros((3, 3), dtype=int)

    # Fill the output grid with red square number follow specific pattern sequence:
    # 1. Fill the top row, then the next row, but skip every other column.
    # 2. Begin the first/third/fifth/etc row in the first column, but begin the second/forth/etc row in the second column.
    pos_list = []
    for i in range(9):
        if i % 2 == 0:
            pos_list.append((i % 3, i // 3))

    # Place the same number of 1 x 1 blue squares on the output grid follow the specific pattern sequence.
    for i in range(num_red_square):
        x, y = pos_list[i]
        output_grid[x, y] = Color.BLUE
        
    return  output_grid

def generate_input():
    # Generate the background grid with size of n x n.
    square_len = np.random.randint(3, 10)
    n, m = square_len, square_len
    grid = np.zeros((n, m), dtype=int)

    # Generate the 2 x 2 red squares on the grid.
    square = random_sprite(n=2, m=2, color_palette=[Color.RED], density=1.0)

    # Randomly choose the number of 2 x 2 red squares.
    square_num = np.random.randint(1, 6)

    # Place the 2 x 2 red squares on the grid.
    for _ in range(square_num):
        # Make sure there is enough space for the 2 x 2 red square.
        try:
            # Place the 2 x 2 red square on the grid.
            # Make sure the red square is not too close to each other.
            x, y = random_free_location_for_sprite(grid=grid, sprite=square, padding=1, padding_connectivity=4)
            grid = blit_sprite(grid=grid, sprite=square, x=x, y=y)
        except:
            break
    return grid

# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)
