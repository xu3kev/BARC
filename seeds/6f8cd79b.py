from common import *

import numpy as np
from typing import *

# concepts:
# borders

# description:
# In the input you will see an empty black grid.
# To make the output, draw a line along the border of the input with a thickness of one pixel. The border should be teal.

def main(input_grid):
    # make the output grid
    n, m = input_grid.shape
    output_grid = np.zeros((n, m), dtype=int)

    # draw the border of the input grid
    draw_line(grid=output_grid, x=0, y=0, length=None, color=Color.TEAL, direction=(1,0))
    draw_line(grid=output_grid, x=n-1, y=0, length=None, color=Color.TEAL, direction=(0,1))
    draw_line(grid=output_grid, x=0, y=0, length=None, color=Color.TEAL, direction=(0,1))
    draw_line(grid=output_grid, x=0, y=m-1, length=None, color=Color.TEAL, direction=(1,0))

    return output_grid
    

def generate_input():
    # make a rectangular black grid
    n = np.random.randint(3, 8)
    m = np.random.randint(3, 8)
    grid = np.zeros((n, m), dtype=int)

    return grid


# ============= remove below this point for prompting =============

if __name__ == '__main__':
    visualize(generate_input, main)