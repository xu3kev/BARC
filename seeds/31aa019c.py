from common import *

import numpy as np
from typing import *

# concepts:
# counting, uniqueness, surrounding

# description:
# In the input, you will see a grid with a black background and colored pixels sprinkled on it. Exactly one color occurs only one time.
# To make the output, find the cell whose color is unique (color occurs only one time), and surround that cell with red pixels. Make all the other pixels black.

def main(input_grid: np.ndarray) -> np.ndarray:
    # Plan:
    # 1. Create a blank new canvas (so that the non-unique colors don't get copied)
    # 2. Find the unique cell
    # 3. Surround the unique cell with red pixels

    output_grid = np.zeros_like(input_grid)

    # 2. Find the unique cell
    unique_color = None
    for color in Color.NOT_BLACK:
        if np.count_nonzero(input_grid == color) == 1:
            unique_color = color
            break
    
    # 3. Surround the unique cell with red pixels
    # First get the coordinates of the unique cell
    x, y, width, height = bounding_box(input_grid == unique_color)
    # Copy red over the region around the unique cell (but this will accidentally delete the unique cell, so be copied back)
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if 0 <= i < len(input_grid) and 0 <= j < len(input_grid[0]):
                output_grid[i, j] = Color.RED
    # Copy the unique cell back
    output_grid[x, y] = unique_color

    return output_grid


    



def generate_input() -> np.ndarray:
    
    # make a 10x10 black grid first as background
    n, m = 10, 10
    grid = np.zeros((n, m), dtype=int)

    # randomly select a unique color from Color.NOT_BLACK
    unique_color = random.choice(Color.NOT_BLACK)

    # randomly choose a non-border cell for the unique color
    non_border_cells = [ (i, j) for i in range(1, n-1) for j in range(1, m-1) ]
    unique_cell = random.choice(non_border_cells)
    grid[unique_cell] = unique_color

    # remove the unique color from the list
    remaining_colors = [ color for color in Color.NOT_BLACK if color != unique_color ]

    for remaining_color in remaining_colors:
        # Pick a random frequency but make sure that this colour is not unique (does not have frequency 1)
        frequency_of_this_color = random.choice([0, 2, 3, 4, 5, 6])

        for _ in range(frequency_of_this_color):
            # randomly choose an unoccupied cell for the remaining color
            empty_cells = [ (i, j) for i in range(n) for j in range(m) if grid[i][j] == Color.BLACK ]
            x, y = random.choice(empty_cells)
            grid[x, y] = remaining_color
    
    return grid
  



# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)